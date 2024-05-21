from pyairtable import Api
from pyairtable.formulas import match, to_airtable_value
from pyairtable.orm import Model, fields as F

# class SchoolYear(Model):
#     name = F.TextField("Name")
#     start_date = F.DateField("Start Date")
#     end_date = F.DateField("End Date")
#     grade = F.IntegerField("Grade")

# class Course(Model):
#     name = F.TextField("Name")
#     school_year = F.LinkField("School Year", SchoolYear)
#     code = F.TextField("Code")
#     data_id = F.TextField("Data ID")
#     html_prefix = F.TextField("HTML Prefix")

# class Assignment(Model):
#     data_id = F.TextField("Data ID")
#     course = F.LinkField("Course", Course)
#     category = F.SelectField("Category")
#     quarter = F.TextField("Quarter")
#     title = F.TextField("Title")
#     date_due = F.DateField("Date Due")
#     comment = F.TextField("Comment")
#     awarded_grade = F.FloatField("Awarded Grade")
#     max_grade = F.FloatField("Max Grade")
#     status = F.SelectField("Status")

def get_airtable_api(personal_access_token):
    return Api(personal_access_token)

def get_active_courses_from_airtable(api, base_id, table_id):
    table = api.table(base_id, table_id)
    formula = match({"Active": 1})
    return [record for record in table.iterate(page_size=100, max_records=1000, formula=formula, fields=["Name", "HTML ID"])][0]

def get_active_assignments_from_airtable(api, base_id, table_id):
    table = api.table(base_id, table_id)
    formula = match({"Active": 1})
    return [record for record in table.iterate(page_size=100, max_record=1000, formula=formula, fields=["Data ID", "Course", "Category", "Quarter", "Title", "Date Due", "Comment", "Awarded Grade", "Max Grade", "Status"])]

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