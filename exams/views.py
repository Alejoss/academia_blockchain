from django.shortcuts import render


def exams_index(request):
    template = "exams/exams.html"
    context = {}
    return render(request, template, context)
