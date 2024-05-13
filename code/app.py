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
    
    assignments = get_assignments(session, courses)

    with Session() as session:
        for assignment in assignments:
            try:
                session.add(assignment)
                session.commit()
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
                
                

if __name__ == "__main__":
    main()