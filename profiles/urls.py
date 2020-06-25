from django.urls import path
from django.contrib.auth import views as auth_views

from profiles import views

urlpatterns = [
    path('profile_data/', views.profile_data, name="profile_data"),
    path('profile_security/', views.profile_security, name="profile_security"),
    path('profile_courses/', views.profile_courses, name="profile_courses"),
    path('profile_accreditation/', views.profile_accreditation, name="profile_accreditation"),
    path('profile_certificates/', views.profile_certificates, name="profile_certificates"),
    path('profile_content/', views.profile_content, name="profile_content"),

    path('content/', views.content, name="content"),
    path('login/', views.HTMLLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView, name="logout"),

    # api
    path('login/', views.api_create_profile, name="create_profile"),
]
