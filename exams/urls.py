from django.urls import path
from exams import views

urlpatterns = [
    path('', views.html_exams_index, name="exams_index"),
    path('create_exams', views.html_create_exam, name="html_create_exams"),

    # api
    path('api/exams/', views.api_exams, name="api_exams"),
    path('api/create/', views.api_create_exam, name="api_create_exam"),
]
