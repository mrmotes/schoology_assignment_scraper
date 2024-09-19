import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from pyairtable import Api
from pyairtable.formulas import match, to_airtable_value

load_dotenv()

api = Api(os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN'))
base_id = os.getenv('AIRTABLE_BASE_ID')

course_table_id = os.getenv('AIRTABLE_COURSE_TABLE_ID')
course_table = api.table(base_id, course_table_id)

assignment_table_id = os.getenv('AIRTBALE_ASSIGNMENT_TABLE_ID')
assignment_table = api.table(base_id, assignment_table_id)
assignment_keys = ['Course', 'Title', 'Date Due', 'Comment', 'Awarded Grade', 'Max Grade', 'Status']

def get_active_airtable_courses():
    formula = match({'Active': 1})
    fields = ['Name', 'HTML ID']
    return [record for record in course_table.iterate(page_size=100, max_records=1000, formula=formula, fields=fields)][0]

def sync_assignment_with_airtable(assignment):
    formula = match({'Data ID': assignment['Data ID']})
    existing_record = assignment_table.first(formula=formula)

    assignment['Course'] = [assignment['Course']]
    assignment['Date Due'] = to_airtable_value(assignment['Date Due'])

    if existing_record:
        if has_changes(existing_record, assignment):
            assignment_table.update(existing_record['id'], assignment)
            logging.info(f'🔄 Updated Record: {existing_record['fields']['Data ID']}')
        else:
            logging.info(f'😴 No Changes: {existing_record['fields']['Data ID']}')
    else:
        assignment_table.create(assignment)
        logging.info(f'🌱 Created Record: {assignment['Data ID']}')


def has_changes(existing_assignment, new_assignment):
    for key in assignment_keys:
        existing_value = existing_assignment['fields'].get(key)
        new_value = None if new_assignment[key] == "" else new_assignment[key]

        if isinstance(existing_value, datetime) and isinstance(new_value, datetime):
            existing_value = existing_value.replace(microsecond=0)
            new_value = new_value.replace(microsecond=0)

        if existing_value != new_value:
             return True

    return False