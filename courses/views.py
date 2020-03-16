from django.shortcuts import render


def course_index(request):
    template = "templates/courses.html"
    context = {}
    return render(request, template, context)
