from http import HTTPStatus
import json

from django.shortcuts import render
from django.http import HttpResponse

from exams.models import Exam
from profiles.models import Profile


def exam_index(request):
    template = "exams/exams_index.html"
    context = {"exam_index_active": "active"}
    return render(request, template, context)


def exam(request):
    template = "exams/exam.html"
    context = {"exam_index_active": "active"}
    return render(request, template, context)


def exam_manage(request):
    template = "exams/exam_manage.html"
    context = {"exam_index_active": "active"}
    return render(request, template, context)


def html_create_exam(request):
    template = "courses/create_exam.html"
    context = {}
    return render(request, template, context)


def api_create_exam(request):
    if request.is_ajax() and request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        accreditor = Profile.objects.get(user=request.user)
        Exam.objects.create(title=title, description=description, accreditor=accreditor)

        return HttpResponse(status=HTTPStatus.OK)
    else:
        return HttpResponse(status=HTTPStatus.FORBIDDEN)


def api_exams(request):
    all_exams = Exam.objects.all()
    exams_dict = {}

    for exam in all_exams:
        exam_data = {"title": exam.title, "description": exam.description, "accreditor": exam.accreditor.user.username}
        exams_dict[exam.id] = exam_data

    return HttpResponse(json.dumps(exams_dict))
