import logging
import os
import time
from airtable import get_active_airtable_courses, sync_assignment_with_airtable
from schoology_scraper import login_to_schoology, get_schoology_assignments

start_time = time.time()


# --- Cross-platform Logging Setup ---
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, 'logs', 'cron_logs.txt')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    session = login_to_schoology()
    if not session:
        logging.error('❌ Login Error: Unable to establish a connection with Schoology')
        return

    airtable_courses = get_active_airtable_courses()
    
    if len(airtable_courses) == 0:
        logging.info('😎 No School: Schools out for summer!')
        return

    schoology_assignments = get_schoology_assignments(session, airtable_courses)

    for schoology_assignment in schoology_assignments:
        sync_assignment_with_airtable(schoology_assignment)


if __name__ == "__main__":
    main()

    end_time = time.time()

    elapsed_time = end_time - start_time
    logging.info(f'⏳ Execution Time: {elapsed_time:.2f} seconds')