from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

school_router = DefaultRouter()
student_router = DefaultRouter()
course_router = DefaultRouter()

school_router.register(r'schools', SchoolViewSet, basename='school')
student_router.register(r'students', StudentViewSet, basename='student')
course_router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(school_router.urls)),
    path('', include(student_router.urls)),
    path('', include(course_router.urls))
]

# urlpatterns = [
#     path(r'schools/', SchoolList.as_view(), name='school_list'),
#     path(r'schools/list', ListSchools.as_view(), name='list_schools'),
#     path(r'schools/<int:pk>/', SchoolDetail.as_view(), name='school_detail'),
#     path(r'schools/<int:pk>/students/', SchoolStudents.as_view(), name='school_students'),
#
#     path(r'courses/', CourseList.as_view(), name='course_list'),
#     path(r'courses/notIn', SpecificCourse.as_view(), name='notIn_course'),
#     path(r'courses/<int:pk>/', CourseDetail.as_view(), name='course_detail'),
#     path(r'courses/lst', ListCoursesStudent.as_view(), name='course_student'),
#
#     path(r'students/', StudentList.as_view(), name='student_list'),
#     path(r'students/<int:pk>/', StudentDetail.as_view(), name='student_detail'),
# ]
