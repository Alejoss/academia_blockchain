from http import HTTPStatus

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse


class HTMLLoginView(LoginView):

    template_name = "profiles/login.html"


def content(request):
    template = "profiles/content.html"
    context = {"content_index_active": "active"}
    return render(request, template, context)


def profile_data(request):
    template = "profiles/profile_data.html"
    context = {"profile_index_active": "active"}
    return render(request, template, context)


def profile_security(request):
    template = "profiles/profile_security.html"
    context = {"profile_index_active": "active"}
    return render(request, template, context)


def profile_courses(request):
    template = "profiles/profile_courses.html"
    context = {"profile_index_active": "active"}
    return render(request, template, context)


def profile_accreditation(request):
    template = "profiles/profile_accreditations.html"
    context = {"profile_index_active": "active"}
    return render(request, template, context)


def profile_certificates(request):
    template = "profiles/profile_certificates.html"
    context = {"profile_index_active": "active"}
    return render(request, template, context)


def profile_content(request):
    template = "profiles/profile_content.html"
    context = {"profile_index_active": "active"}
    return render(request, template, context)


def api_create_profile(request):
    if request.is_ajax() and request.method == "POST":
        template = "profiles/create_profile_succesfull.html"
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username, email, password)
        # TODO send email to confirm account
        return render(request, template, {"user": user})
    else:
        return HttpResponse(status=HTTPStatus.FORBIDDEN)


def complete_account(request):  # TODO implement % complete profile?
    pass
