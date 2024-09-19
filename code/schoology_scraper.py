import logging
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv


def get_schoology_assignments(session, courses):

    grades_url = 'https://app.schoology.com/parent/grades_attendance/grades'
    response = session.get(grades_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    assignments = []

    for course in courses:
        course_html_id = course['fields']['HTML ID']
        course_gradebook_div = soup.find('div', id=course_html_id)
        if not course_gradebook_div:
            print(f'NotFound: {course_html_id}')

        gradebook_course_grades_div = course_gradebook_div.find('div', class_='gradebook-course-grades')
        table_rows = gradebook_course_grades_div.find_all('tr')

        current_quarter = ''
        current_category = ''
        
        for tr in table_rows:
            tr_html_classes = tr.get('class')
            if 'item-row' in tr_html_classes:
                assignment_details = get_assignment_from_table_row(tr)
                assignment = {
                    'Data ID': tr.get('data-id') ,
                    'Course': course['id'], 
                    'Category': current_category, 
                    'Quarter': current_quarter, 
                    'Title': assignment_details.get('title'), 
                    'Date Due': assignment_details.get('due_date'), 
                    'Comment': assignment_details.get('comment'), 
                    'Awarded Grade': assignment_details.get('awarded_grade'), 
                    'Max Grade': assignment_details.get('max_grade'), 
                    'Status': assignment_details.get('status')
                }
                assignments.append(assignment)
            elif 'period-row' in tr_html_classes:
                current_quarter = get_title_from_table_row(tr)
            elif 'category-row' in tr_html_classes:
                current_category = get_title_from_table_row(tr)

    return assignments


def login_to_schoology():
    load_dotenv()
    login_url = 'https://app.schoology.com/login'
    credentials = {
        'mail': os.getenv('USERNAME'),  
        'pass': os.getenv('PASSWORD'),
        'school_nid': os.getenv('SCHOOL_ID'),
        'form_build_id': os.getenv('FORM_BUILD_ID'),
        'form_id': os.getenv('FORM_ID')
    }
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'}) 
    try:
        response = session.post(login_url, data=credentials)
        response.raise_for_status()

        if 'login_error' in response.text:
            raise Exception('Login failed. Check your credentials or the Schoology website.')

        logging.info('✅ Successfully logged into Schoology')
        return session
    except requests.exceptions.HTTPError as errh:
        logging.error(f'❌ HTTPError: {errh}')
    except requests.exceptions.ConnectionError as errc:
        logging.error(f'❌ ConnectionError: {errc}')
    except requests.exceptions.Timeout as errt:
        logging.error(f'❌ Timeout: {errt}')
    except requests.exceptions.RequestException as err:
        logging.error(f'❌ RequestException: {err}')

    return None


def get_grade_string_as_float(grade_string):
    if not grade_string:
        return None
    
    return float(''.join(char for char in grade_string if char.isdigit() or char == '.'))


def get_due_date_string_as_date(due_date_string):
    match = re.search(r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b', due_date_string)
    if match:
        try:
            return datetime.strptime(match.group(1), '%m/%d/%y').date()
        except ValueError:
            pass
    return None


def get_grade_details(grade_column):
    if not grade_column:
        return None

    grade_details = {
        'awarded-grade': 0.0,
        'max-grade': 0.0,
        'status': 'Pending'
    }

    awarded_grade = grade_column.find('span', class_='awarded-grade')

    if awarded_grade:
        grade_details['awarded-grade'] = get_grade_string_as_float(awarded_grade.text)
        max_grade = grade_column.find('span', class_='max-grade')
        if max_grade:
            grade_details['max-grade'] = get_grade_string_as_float(max_grade.text)
        grade_details['status'] = 'Complete'
        return grade_details
    
    no_grade = grade_column.find('span', class_='no-grade')

    if no_grade:
        status = grade_column.find('span', class_='exception-text')
        if status:
            grade_details['status'] = status.text
            return grade_details
    
    return grade_details


def clean_assignment_comment(comment):
    cleaned_comment = re.sub(r'^Comment:\s*', '', comment, flags=re.IGNORECASE)
    if cleaned_comment == 'No comment':
        cleaned_comment = ''
    return cleaned_comment


def clean_assignment_title(title):
    return re.sub(r'^Note:\s*', '', title, flags=re.IGNORECASE)


def get_assignment_from_table_row(tr):
    title = clean_assignment_title(tr.find('span', class_='title').text)
    due_date = tr.find('span', class_='due-date')
    comment = clean_assignment_comment(tr.find('td', class_='comment-column').text)
    
    if due_date:
        due_date = get_due_date_string_as_date(due_date.text)
    
    grade_colum_td = tr.find('td', class_='grade-column')
    grade_details = get_grade_details(grade_colum_td)

    
    return {
        'data_id': tr.get('data-id'),
        'title': title,
        'due_date': due_date,
        'comment': comment,
        'awarded_grade': grade_details['awarded-grade'],
        'max_grade': grade_details['max-grade'],
        'status': grade_details['status']
    }


def get_title_from_table_row(tr):
    title_span = tr.find('span', class_='title')
    if not title_span:
        return None
    
    title_text = title_span.find(text=True, recursive=False)
    return title_text.strip() if title_text else None
