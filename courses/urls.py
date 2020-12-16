from django.urls import path
from courses import views

urlpatterns = [
    path('', views.event_index, name="event_index"),
    path('event_detail/<int:event_id>', views.event_detail, name="event_detail"),
    path('edit_event/<int:event_id>', views.edit_event, name="edit_event"),
    path('create/', views.event_create, name="event_create"),
    path('delete/<int:event_id>', views.event_delete, name="event_delete"),

    # API
    path('event_bookmark/<int:event_id>', views.event_bookmark, name="event_bookmark"),
    path('remove_bookmark/<int:event_id>', views.remove_bookmark, name="remove_bookmark"),
    path('request_certificate/<int:event_id>', views.request_certificate, name="request_certificate"),
    path('cancel_cert_request/<int:event_id>', views.cancel_cert_request, name="cancel_cert_request"),
    path('accept_certificate/<int:cert_request_id>', views.accept_certificate, name="accept_certificate"),
    path('reject_certificate/<int:cert_request_id>', views.reject_certificate, name="reject_certificate"),
]
