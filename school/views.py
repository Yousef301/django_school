from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from marshmallow import ValidationError
from sqlalchemy import func, and_
from .schemas import *

school_schema = SchoolSchema()
student_schema = StudentSchema()
course_schema = CourseSchema()


class SchoolViewSet(viewsets.ViewSet):
    def list(self, request):
        schools = session.query(School).all()
        result = school_schema.dump(schools, many=True)
        return Response(result)

    def create(self, request):
        try:
            school = school_schema.load(request.data, session=session)
            session.add(school)
            session.commit()
            return Response(request.data, status=status.HTTP_201_CREATED)

        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        school = session.get(School, pk)
        if school:
            result = school_schema.dump(school)
            return Response(result)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        school = session.get(School, pk)
        if school:
            try:
                updated = school_schema.load(request.data, instance=school, session=session)
                session.commit()
                return Response(school_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        school = session.get(School, pk)
        if school:
            try:
                updated = school_schema.load(request.data, instance=school, session=session, partial=True)
                session.commit()
                return Response(school_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        school = session.get(School, pk)
        if school:
            session.delete(school)
            session.commit()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    # 2- schools name that has more than # students
    @action(detail=False, methods=['GET'])
    def list_schools(self, request):
        limit = request.GET.get('students')
        schools = session.query(School.name).outerjoin(Student, Student.school == School.schoolID).group_by(
            School.schoolID).having(func.count(School.schoolID) >= limit).all()
        if schools:
            result = school_schema.dump(schools, many=True)
            return Response(result)

        return Response({"message": "No schools found"}, status=status.HTTP_404_NOT_FOUND)

    # 4- All students and there courses for a specific school
    @action(detail=True, methods=['GET'])
    def students_with_courses(self, request, pk=None):
        school = session.get(School, pk)
        try:
            schema = StudentSchema(exclude=['schools', 'school'])
            result = schema.dump(school.students, many=True)
            return Response(result)

        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)


class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        students = session.query(Student).all()
        result = student_schema.dump(students, many=True)
        return Response(result)

    def create(self, request):
        try:
            student = student_schema.load(request.data, session=session)
            session.add(student)
            session.commit()
            return Response(request.data, status=status.HTTP_201_CREATED)

        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        student = session.get(Student, pk)
        if student:
            result = student_schema.dump(student)
            return Response(result)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        student = session.get(Student, pk)
        if student:
            try:
                updated = student_schema.load(request.data, instance=student, session=session)
                session.commit()
                return Response(student_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        student = session.get(Student, pk)
        if student:
            try:
                updated = student_schema.load(request.data, instance=student, session=session, partial=True)
                session.commit()
                return Response(student_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        student = session.get(Student, pk)
        if student:
            session.delete(student)
            session.commit()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    # 1- list courses for specific student
    @action(detail=True, methods=['GET'])
    def lst_courses(self, request, pk=None):
        courses = session.query(Course).outerjoin(StudentCourse, StudentCourse.c.courseID == Course.courseID).outerjoin(
            Student, Student.studentID == StudentCourse.c.studentID).where(Student.studentID == pk)
        if courses:
            try:
                schema = CourseSchema(exclude=['students'])
                return Response(schema.dump(courses, many=True), status=status.HTTP_200_OK)

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)


class CourseViewSet(viewsets.ViewSet):
    def list(self, request):
        courses = session.query(Course).all()
        result = course_schema.dump(courses, many=True)
        return Response(result)

    def create(self, request):
        try:
            course = course_schema.load(request.data, session=session)
            session.add(course)
            session.commit()
            return Response(request.data, status=status.HTTP_201_CREATED)

        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        course = session.get(Course, pk)
        if course:
            result = course_schema.dump(course)
            return Response(result)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        course = session.get(Course, pk)
        if course:
            try:
                updated = course_schema.load(request.data, instance=course, session=session)
                session.commit()
                return Response(course_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        course = session.get(Course, pk)
        if course:
            try:
                updated = course_schema.load(request.data, instance=course, session=session, partial=True)
                session.commit()
                return Response(course_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        course = session.get(Course, pk)
        if course:
            session.delete(course)
            session.commit()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    # 3- Students that doesn't take a specific course
    @action(detail=True, methods=['GET'])
    def not_in(self, request, pk=None):
        course = session.get(Course, pk)
        if course:
            students = session.query(Student).outerjoin(StudentCourse,
                                                        StudentCourse.c.studentID == Student.studentID).outerjoin(
                Course, and_(Course.courseID == StudentCourse.c.courseID, Course.name == course.name)).group_by(
                Student.studentID).having(func.count(Course.name) == 0).all()

            if students:
                try:
                    schema = StudentSchema(exclude=['courses', 'schools'])
                    result = schema.dump(students, many=True)
                    return Response(result, status=status.HTTP_200_OK)

                except ValidationError as err:
                    return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_404_NOT_FOUND)
