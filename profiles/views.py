from django.shortcuts import render


def profile(request):
    template = "templates/profile.html"
    context = {}
    return render(request, template, context)
