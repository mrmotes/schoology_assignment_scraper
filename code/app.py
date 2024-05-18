import os
import logging
from airtable import get_active_courses_from_airtable, get_airtable_api, sync_assignment_with_airtable
from schoology_scraper import login_to_schoology, get_assignment_data_from_schoology, compare_and_log_changes
from models import Assignment
from database import Session

logging.basicConfig(
    filename='/Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    session = login_to_schoology()
    if not session:
        print('Unable to establish a connection with Schoology.')
        return
    
    api = get_airtable_api(os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN'))
    base_id = os.getenv('AIRTABLE_BASE_ID')
    assignment_table_id = os.getenv('AIRTBALE_ASSIGNMENT_TABLE_ID')
    course_table_id = os.getenv('AIRTABLE_COURSE_TABLE_ID')

    courses = get_active_courses_from_airtable(api, base_id, course_table_id)
    
    if len(courses) == 0:
        logging.info('Schools out for summer!')
        return
    
    updated = 0
    created = 0

    logging.info('Succesfully retrieved Courses from Airtable')
    assignments = get_assignment_data_from_schoology(session, courses)

    with Session() as session:
        for assignment in assignments:
            existing_assignment = session.query(Assignment).filter_by(data_id=assignment.data_id).first()
            if existing_assignment:
                changes_made = compare_and_log_changes(existing_assignment, assignment, session)
                if changes_made:
                    session.commit()
                    sync_assignment_with_airtable(api, base_id, assignment_table_id, existing_assignment)
                    updated += 1
                    logging.info(f'Successfully updated {assignment.data_id} in Airtable')
            else:
                session.add(assignment)
                session.commit()
                sync_assignment_with_airtable(api, base_id, assignment_table_id, assignment)
                created += 1
    
    logging.info(f"Assignments created: {created}")
    logging.info(f"Assignments updated: {updated}")

if __name__ == "__main__":
    main()