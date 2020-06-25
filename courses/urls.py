from django.urls import path
from courses import views

urlpatterns = [
    path('', views.course_index, name="course_index"),
    path('event_singular_localized/', views.event_singular_localized, name="event_singular_localized"),
    path('event_recorded_online/', views.event_recorded_online, name="event_recorded_online"),
    path('event_recurrent_localized/', views.event_recurrent_localized, name="event_recurrent_localized"),
    path('event_singular_online/', views.event_singular_online, name="event_singular_online"),
    path('create/', views.html_create_course, name="html_create_course"),

    # api
    path('api/courses/', views.api_courses, name="api_courses"),
    path('api/create/', views.api_create_course, name="api_create_course"),
]
