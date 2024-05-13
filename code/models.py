from sqlalchemy import create_engine, Boolean, Column, Date, DateTime, Integer, String 
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///schoology.db')
Base = declarative_base()

class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True)
    data_id = Column(String, nullable=False, unique=True)
    course = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quarter = Column(String, nullable=False)
    title = Column(String, nullable=True)
    due_date = Column(Date)
    comment = Column(String)
    awarded_grade = Column(Integer, nullable=True)
    max_grade = Column(Integer, nullable=True)
    status = Column(String)
    date_extracted = Column(DateTime, nullable=False)
    date_last_updated = Column(DateTime, nullable=True)


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    data_id = Column(String, nullable=False, unique=True)
    html_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)


class ChangeLog(Base):
    __tablename__ = 'change_log'

    id = Column(Integer, primary_key=True)
    data_id = Column(String, nullable=False)
    attribute = Column(String, nullable=False)
    previous_value = Column(String, nullable=False)
    new_value = Column(String, nullable=False)
    date_changed = Column(DateTime, nullable=False)

Base.metadata.create_all(engine)