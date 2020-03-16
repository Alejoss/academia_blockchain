from django.shortcuts import render


def exams_index(request):
    template = "templates/exams.html"
    context = {}
    return render(request, template, context)
