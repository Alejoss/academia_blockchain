import json
from http import HTTPStatus

from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from courses.models import Course, AcceptedCrypto

"""
HTML RENDERS
"""


def html_course_index(request):
    template = "courses/courses.html"
    all_courses = Course.objects.all()
    context = {"courses": all_courses}
    return render(request, template, context)


def html_create_course(request):
    template = "courses/create_course.html"
    context = {}
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
        print(accepted_cryptos)
        course = Course.objects.create(title=title, description=description, geolocation=geolocation)

        for c in accepted_cryptos:
            if AcceptedCrypto.objects.filter(code=course).exists():
                course.accepted_cryptos.add(c)

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
