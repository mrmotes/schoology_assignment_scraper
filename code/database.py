from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////Users/motes/Projects/schoology_assignment_scraper/schoology.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)