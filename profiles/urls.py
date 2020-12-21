from django.urls import path
from django.contrib.auth import views as auth_views

from profiles import views

urlpatterns = [
    path('profile_data/', views.profile_data, name="profile_data"),
    path('user_profile/<int:profile_id>', views.user_profile, name="user_profile"),
    path('profile_security/', views.profile_security, name="profile_security"),
    path('profile_events/', views.profile_events, name="profile_events"),
    path('profile_certificates/', views.profile_certificates, name="profile_certificates"),
    path('profile_content/', views.profile_content, name="profile_content"),

    path('profile_edit_picture/', views.profile_edit_picture, name="profile_edit_picture"),
    path('profile_edit_contact/', views.profile_edit_contact, name="profile_edit_contact"),
    path('profile_edit_cryptos/', views.profile_edit_cryptos, name="profile_edit_cryptos"),
    path('profile_bookmarks/', views.profile_bookmarks, name="profile_bookmarks"),
    path('profile_cert_requests/', views.profile_cert_requests, name="profile_cert_requests"),
    path('content/', views.content, name="content"),  # Proximamente

    # manejo de cuentas
    path('register/', views.register_profile, name="profile_register"),
    path('login/', views.AcademiaLogin.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]
