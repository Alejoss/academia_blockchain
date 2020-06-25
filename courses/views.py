from http import HTTPStatus
import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from courses.models import Course, AcceptedCrypto

"""
HTML RENDERS
"""


def course_index(request):
    template = "courses/courses.html"
    all_courses = Course.objects.all()
    context = {"courses": all_courses, "course_index_active": "active"}
    return render(request, template, context)


def event_singular_localized(request):
    template = "courses/event_singular_localized.html"
    context = {"course_index_active": "active"}
    return render(request, template, context)


def event_recorded_online(request):
    template = "courses/event_recorded_online.html"
    context = {"course_index_active": "active"}
    return render(request, template, context)


def event_recurrent_localized(request):
    template = "courses/event_recurrent_localized.html"
    context = {"course_index_active": "active"}
    return render(request, template, context)


def event_singular_online(request):
    template = "courses/event_singular_online.html"
    context = {"course_index_active": "active"}
    return render(request, template, context)


def html_create_course(request):
    template = "courses/create_course.html"
    context = {"course_index_active": "active"}
    return render(request, template, context)


"""
API CALLS
"""


def api_create_course(request):
    if request.is_ajax() and request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        geolocation = request.POST.get("geolocation")
        accepted_cryptos = request.POST.get("accepted_cryptos", [])
        course = Course.objects.create(title=title, description=description, geolocation=geolocation)
        # TODO add creator of the course

        for c in accepted_cryptos:
            code = c.upper()
            if AcceptedCrypto.objects.filter(code=c.upper()).exists():
                accepted_crypto = AcceptedCrypto.objects.get(code=c.upper())
                print(accepted_crypto)
                course.accepted_cryptos.add(accepted_crypto)

        return HttpResponse(status=HTTPStatus.OK)
    else:
        return HttpResponse(status=HTTPStatus.FORBIDDEN)


def api_courses(request):
    all_courses = Course.objects.all()
    courses_dict = {}

    for course in all_courses:
        course_data = {"title": course.title, "description": course.description, "geolocation": course.geolocation,
                       "accepted_cryptos": course.get_actepted_cryptos}
        courses_dict[course.id] = course_data

    return HttpResponse(json.dumps(courses_dict))
