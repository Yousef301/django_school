import os

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from marshmallow import ValidationError
from .compnents import *
from .schemas import *

school_schema = SchoolSchema()
student_schema = StudentSchema()
course_schema = CourseSchema()


class SchoolViewSet(viewsets.ViewSet):
    def list(self, request):
        schools = SchoolQueries().list_schools()
        result = school_schema.dump(schools, many=True)
        return Response(result)

    def create(self, request):
        try:
            school = school_schema.load(request.data, session=session)
            SchoolQueries().add_school(school)
            return Response(request.data, status=status.HTTP_201_CREATED)

        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        school = SchoolQueries().school(pk)
        if school:
            result = school_schema.dump(school)
            return Response(result)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        school = SchoolQueries().school(pk)
        if school:
            try:
                updated = school_schema.load(request.data, instance=school, session=session)
                commit()
                return Response(school_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        school = SchoolQueries().school(pk)
        if school:
            try:
                updated = school_schema.load(request.data, instance=school, session=session, partial=True)
                commit()
                return Response(school_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        school = SchoolQueries().school(pk)
        if school:
            SchoolQueries().delete_school(school)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    # 2- schools name that has more than # students
    @action(detail=False, methods=['GET'])
    def list_schools(self, request):
        limit = request.GET.get('students')
        schools = SchoolQueries().schools_by_students(limit)
        if schools:
            result = school_schema.dump(schools, many=True)
            return Response(result)

        return Response({"message": "No schools found"}, status=status.HTTP_404_NOT_FOUND)

    # 4- All students and there courses for a specific school
    @action(detail=True, methods=['GET'])
    def students_with_courses(self, request, pk=None):
        school = SchoolQueries().school(pk)
        if school:
            try:
                schema = StudentSchema(exclude=['schools', 'school'])
                result = schema.dump(school.students, many=True)
                file_name = to_csv(result, school.name.lower())
                path = os.path.abspath(file_name)

                upload_to_s3(file_name, 'school-bucket-s3', path)

                return Response(result)

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)


class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        students = StudentQueries().list_students()
        result = student_schema.dump(students, many=True)
        return Response(result)

    def create(self, request):
        try:
            student = student_schema.load(request.data, session=session)
            StudentQueries().add_student(student)
            return Response(request.data, status=status.HTTP_201_CREATED)

        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        student = StudentQueries().student(pk)
        if student:
            result = student_schema.dump(student)
            return Response(result)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        student = StudentQueries().student(pk)
        if student:
            try:
                updated = student_schema.load(request.data, instance=student, session=session)
                commit()
                return Response(student_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        student = StudentQueries().student(pk)
        if student:
            try:
                updated = student_schema.load(request.data, instance=student, session=session, partial=True)
                commit()
                return Response(student_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        student = StudentQueries().student(pk)
        if student:
            StudentQueries().delete_student(student)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    # 1- list courses for specific student
    @action(detail=True, methods=['GET'])
    def lst_courses(self, request, pk=None):
        courses = CourseQueries().list_courses_by_student(pk)
        if courses:
            try:
                schema = CourseSchema(exclude=['students'])
                return Response(schema.dump(courses, many=True), status=status.HTTP_200_OK)

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)


class CourseViewSet(viewsets.ViewSet):
    def list(self, request):
        courses = CourseQueries().list_courses()
        result = course_schema.dump(courses, many=True)
        return Response(result)

    def create(self, request):
        try:
            course = course_schema.load(request.data, session=session)
            CourseQueries().add_course(course)
            return Response(request.data, status=status.HTTP_201_CREATED)

        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        course = CourseQueries().course(pk)
        if course:
            result = course_schema.dump(course)
            return Response(result)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        course = CourseQueries().course(pk)
        if course:
            try:
                updated = course_schema.load(request.data, instance=course, session=session)
                commit()
                return Response(course_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        course = CourseQueries().course(pk)
        if course:
            try:
                updated = course_schema.load(request.data, instance=course, session=session, partial=True)
                commit()
                return Response(course_schema.dump(updated))

            except ValidationError as err:
                return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        course = CourseQueries().course(pk)
        if course:
            CourseQueries().delete_course(course)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    # 3- Students that doesn't take a specific course
    @action(detail=True, methods=['GET'])
    def not_in(self, request, pk=None):
        course = CourseQueries().course(pk)
        if course:
            students = StudentQueries().students_not_in_course(course.name)

            if students:
                try:
                    schema = StudentSchema(exclude=['courses', 'schools'])
                    result = schema.dump(students, many=True)
                    return Response(result, status=status.HTTP_200_OK)

                except ValidationError as err:
                    return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_404_NOT_FOUND)
