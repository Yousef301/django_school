from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from school.models import *
from marshmallow import fields


class SchoolSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = session
        model = School
        include_relationships = True
        load_instance = True


class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = session
        model = Course
        include_relationships = True
        load_instance = True


class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = session
        model = Student
        include_fk = True
        load_instance = True

    schools = fields.Nested(SchoolSchema, many=False, exclude=('students',))
    courses = fields.Nested(CourseSchema, many=True, exclude=('students',))

# student_schema = StudentSchema()
# students = session.query(Student).all()
# student_data_list1 = student_schema.dump(students, many=True)
# student_data_list2 = student_schema.dumps(students, many=True)
# print(type(student_data_list1))
# print(type(student_data_list2))
# stu = student_schema.load(student_data_list1, session=session, many=True)
# print(stu)
