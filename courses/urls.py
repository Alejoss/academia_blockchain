from django.urls import path
from courses import views

urlpatterns = [
    path('', views.event_index, name="event_index"),
    path('about/', views.about, name="about"),
    path('events_tag/<int:tag_id>', views.events_tag, name="events_tag"),
    path('events_all/', views.events_all, name="events_all"),
    path('event_search/', views.event_search, name="event_search"),
    path('event_detail/<int:event_id>', views.event_detail, name="event_detail"),
    path('edit/<int:event_id>', views.event_edit, name="event_edit"),
    path('create/', views.event_create, name="event_create"),
    path('delete/<int:event_id>', views.event_delete, name="event_delete"),
    path('comment/<int:event_id>', views.event_comment, name="event_comment"),
    path('certificate_preview/<int:cert_id>', views.certificate_preview, name="certificate_preview"),
    path('send_cert_blockchain/<int:cert_id>', views.send_cert_blockchain, name="send_cert_blockchain"),
    path('add_cert_hash/<int:cert_id>', views.add_cert_hash, name="add_cert_hash"),


    # API
    path('event_bookmark/<int:event_id>', views.event_bookmark, name="event_bookmark"),
    path('remove_bookmark/<int:event_id>', views.remove_bookmark, name="remove_bookmark"),
    path('certificate_detail/<int:certificate_id>', views.certificate_detail, name="certificate_detail"),
    path('request_certificate/<int:event_id>', views.request_certificate, name="request_certificate"),
    path('cancel_cert_request/<int:cert_request_id>', views.cancel_cert_request, name="cancel_cert_request"),
    path('accept_cert_request/<int:cert_request_id>', views.accept_cert_request, name="accept_cert_request"),
    path('reject_cert_request/<int:cert_request_id>', views.reject_cert_request, name="reject_cert_request"),
    path('restore_cert_request/<int:cert_request_id>', views.restore_cert_request, name="restore_cert_request")
]
