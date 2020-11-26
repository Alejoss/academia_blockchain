from django.urls import path
from courses import views

urlpatterns = [
    path('', views.event_index, name="event_index"),
    path('event_detail/<int:event_id>', views.event_detail, name="event_detail"),
    path('edit_event/<int:event_id>', views.edit_event, name="edit_event"),
    path('event_bookmark/<int:event_id>', views.event_bookmark, name="event_bookmark"),
    path('remove_bookmark/<int:event_id>', views.remove_bookmark, name="remove_bookmark"),
    path('request_certificate/<int:event_id>', views.request_certificate, name="request_certificate"),
    path('cancel_certificate_request/<int:event_id>', views.cancel_certificate_request, name="cancel_certificate_request"),
    path('create/', views.event_create, name="event_create"),

    # api
    # path('api/courses/', views.api_courses, name="api_courses"),
    # path('api/create/', views.api_create_course, name="api_create_course"),
]
