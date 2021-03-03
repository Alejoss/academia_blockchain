from django.urls import path
from courses import views

urlpatterns = [
    path('', views.event_index, name="event_index"),
    path('events_tag/<int:tag_id>', views.events_tag, name="events_tag"),
    path('event_detail/<int:event_id>', views.event_detail, name="event_detail"),
    path('edit/<int:event_id>', views.event_edit, name="event_edit"),
    path('create/', views.event_create, name="event_create"),
    path('delete/<int:event_id>', views.event_delete, name="event_delete"),
    path('comment/<int:event_id>', views.event_comment, name="event_comment"),
    path('certificate_preview/<int:cert_id>', views.certificate_preview, name="certificate_preview"),

    # API
    path('event_bookmark/<int:event_id>', views.event_bookmark, name="event_bookmark"),
    path('remove_bookmark/<int:event_id>', views.remove_bookmark, name="remove_bookmark"),
    path('certificate_detail/<int:certificate_id>', views.certificate_detail, name="certificate_detail"),
    path('request_certificate/<int:event_id>', views.request_certificate, name="request_certificate"),
    path('cancel_cert_request/<int:event_id>', views.cancel_cert_request, name="cancel_cert_request"),
    path('accept_certificate/<int:cert_request_id>', views.accept_certificate, name="accept_certificate"),
    path('reject_certificate/<int:cert_request_id>', views.reject_certificate, name="reject_certificate"),
]
