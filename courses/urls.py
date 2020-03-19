
from django.urls import path
from courses import views

urlpatterns = [
    path('create/', views.html_create_course, name="html_create_course"),
    # api
    path('api/courses/', views.api_courses, name="api_courses"),
    path('api/create/', views.api_create_course, name="api_create_course"),
]
