import os
from pyairtable import Api
from pyairtable.formulas import match, to_airtable_value
from schoology_scraper import login_to_schoology, get_assignments, compare_and_log_changes
from models import Assignment
from database import Session
from sqlalchemy.exc import IntegrityError


def main():
    session = login_to_schoology()
    if not session:
        print('Unable to establish a connection with Schoology.')
        return
    
    api = Api(os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN'))
    base_id = os.getenv('AIRTABLE_BASE_ID')
    assignment_table_id = os.getenv('AIRTBALE_ASSIGNMENT_TABLE_ID')
    course_table_id = os.getenv('AIRTABLE_COURSE_TABLE_ID')

    courses = get_active_courses_from_airtable(api, base_id, course_table_id)
    
    if len(courses) == 0:
        print('Schools out for summer!')
        return
    
    assignments = get_assignments(session, courses)

    with Session() as session:
        for assignment in assignments:
            existing_assignment = session.query(Assignment).filter_by(data_id=assignment.data_id).first()
            if existing_assignment:
                changes_made = compare_and_log_changes(existing_assignment, assignment, session)
                if changes_made:
                    session.commit()
                    sync_assignment_with_airtable(api, base_id, assignment_table_id, existing_assignment)
            else:
                session.add(assignment)
                session.commit()
                sync_assignment_with_airtable(api, base_id, assignment_table_id, assignment)
                

def sync_assignment_with_airtable(api, base_id, table_id, assignment):
    table = api.table(base_id, table_id)
    formula = match({"Data ID": assignment.data_id})
    existing_record = table.first(formula=formula)

    assignment_data = {
                "Data ID": assignment.data_id,
                "Course": [assignment.course],
                "Category": assignment.category,
                "Quarter": assignment.quarter,
                "Title": assignment.title,
                "Date Due": to_airtable_value(assignment.due_date),
                "Comment": assignment.comment,
                "Awarded Grade": assignment.awarded_grade,
                "Max Grade": assignment.max_grade,
                "Status": assignment.status
            }
    if existing_record:
        table.update(existing_record['id'], assignment_data)
    else:
        table.create(assignment_data)

def get_active_courses_from_airtable(api, base_id, table_id):
    table = api.table(base_id, table_id)
    formula = match({"Active": 1})
    return [record for record in table.iterate(page_size=100, max_records=1000, formula=formula, fields=["Name", "HTML ID"])][0]




if __name__ == "__main__":
    main()