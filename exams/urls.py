from django.urls import path
from exams import views

urlpatterns = [
    path('create_exams/', views.html_create_exam, name="html_create_exams"),
    path('exam/', views.exam, name="exam"),
    path('exam_manage/', views.exam_manage, name="exam_manage"),

    # api
    path('api/exams/', views.api_exams, name="api_exams"),
    path('api/create/', views.api_create_exam, name="api_create_exam"),
]
