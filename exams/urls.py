from django.urls import path
from exams import views

urlpatterns = [
    path('', views.exams_index, name="exams_index"),
]
