from sqlalchemy import func, and_

from .models import *


def commit():
    session.commit()


class SchoolQueries:
    def list_schools(self):
        return session.query(School).all()

    def add_school(self, school):
        session.add(school)
        commit()

    def delete_school(self, school):
        session.delete(school)
        commit()

    def school(self, pk):
        return session.get(School, pk)

    def schools_by_students(self, students):
        return session.query(School.name).outerjoin(Student, Student.school == School.schoolID).group_by(
            School.schoolID).having(func.count(School.schoolID) >= students).all()


class StudentQueries:
    def list_students(self):
        return session.query(Student).all()

    def add_student(self, student):
        session.add(student)
        commit()

    def delete_student(self, student):
        session.delete(student)
        commit()

    def student(self, pk):
        return session.get(Student, pk)

    def students_not_in_course(self, course_name):
        return session.query(Student).outerjoin(StudentCourse,
                                                StudentCourse.c.studentID == Student.studentID).outerjoin(
            Course, and_(Course.courseID == StudentCourse.c.courseID, Course.name == course_name)).group_by(
            Student.studentID).having(func.count(Course.name) == 0).all()


class CourseQueries:
    def list_courses(self):
        return session.query(Course).all()

    def add_course(self, course):
        session.add(course)
        commit()

    def delete_course(self, course):
        session.delete(course)
        commit()

    def course(self, pk):
        return session.get(Course, pk)

    def list_courses_by_student(self, pk):
        return session.query(Course).outerjoin(StudentCourse, StudentCourse.c.courseID == Course.courseID).outerjoin(
            Student, Student.studentID == StudentCourse.c.studentID).where(Student.studentID == pk)
