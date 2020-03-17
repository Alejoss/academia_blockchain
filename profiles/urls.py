
from django.urls import path
from exams import views

urlpatterns = [
    path('/', views.profile, name="profile"),
]
