from http import HTTPStatus

from django.shortcuts import render
from django.http import HttpResponse

from courses.models import Course, AcceptedCrypto


def course_index(request):
    template = "courses/courses.html"
    context = {}
    return render(request, template, context)


def create_course(request):

    if request.is_ajax() and request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        geolocation = request.POST.get("geolocation")
        accepted_cryptos = request.POST.get("accepted_cryptos")
        course = Course.objects.create(title=title, description=description, geolocation=geolocation)

        for c in accepted_cryptos:
            if AcceptedCrypto.objects.filter(code=course).exists():
                course.accepted_cryptos.add(c)

        return HttpResponse(status=HTTPStatus.OK)
    else:
        return HttpResponse(status=HTTPStatus.FORBIDDEN)
