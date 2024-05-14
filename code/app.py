import os
from pyairtable import Api
from pyairtable.formulas import match, to_airtable_value
from schoology_scraper import login_to_schoology, get_assignments, compare_and_log_changes
from models import Assignment
from database import Session
from sqlalchemy.exc import IntegrityError

courses = [
    {
        'id': '6803387625',
        'name': 'English Language Arts',
        'code': 'ENG1037',
        'html_id': 's-js-gradebook-course-6803387625'
    },
    {
        'id': '6803388145',
        'name': 'Mathematics',
        'code': 'MTH4007',
        'html_id': 's-js-gradebook-course-6803388145'
    },
    {
        'id': '6803389091',
        'name': 'Science',
        'code': 'SCI6007',
        'html_id': 's-js-gradebook-course-6803389091'
    },
    {
        'id': '6803749517',
        'name': 'Social Studies',
        'code': 'SOC5007',
        'html_id': 's-js-gradebook-course-6803749517'
    }
]


def main():
    session = login_to_schoology()
    if not session:
        print('Unable to establish a connection with Schoology.')
        return
    
    api = Api(os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN'))
    base_id = os.getenv('AIRTABLE_BASE_ID')
    table_id = os.getenv('AIRTBALE_TABLE_ID')
    
    assignments = get_assignments(session, courses)

    with Session() as session:
        for assignment in assignments:
            try:
                session.add(assignment)
                session.commit()
                sync_assignment_with_airtable(api, base_id, table_id, assignment)

            except IntegrityError:
                session.rollback()
                existing_assignment = session.query(Assignment).filter_by(data_id=assignment.data_id).first()
                if existing_assignment:
                    if compare_and_log_changes(existing_assignment, assignment, session):
                        session.commit()
                else:
                    print(f"Error: Existing assignment not found for data_id={assignment.data_id}")
                    for attr, value in assignment.__dict__.items():
                        if not attr.startswith('_'):
                            print(f"{attr}: {value}")
                

def sync_assignment_with_airtable(api, base_id, table_id, assignment):
    table = api.table(base_id, table_id)
    formula = match({"Data ID": assignment.data_id})
    existing_record = table.first(formula=formula)
    assignment_data = {
                "Data ID": assignment.data_id,
                "Course": assignment.course,
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


if __name__ == "__main__":
    main()