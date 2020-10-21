from http import HTTPStatus

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

from profiles.utils import AcademiaUserCreationForm, AcademiaLoginForm
from profiles.models import Profile, AcceptedCrypto
from courses.models import Event


# Manejo de cuentas
def register_profile(request):
    if request.method == "GET":
        template = "profiles/register.html"
        form = AcademiaUserCreationForm
        context = {"form": form}
        return render(request, template, context)

    elif request.method == "POST":
        form = AcademiaUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            # Crear perfil de usuario
            new_profile = Profile.objects.create(user=new_user)
            template = "profiles/profile_data.html"
            context = {'new_profile': new_profile}
            return render(request, template, context)
        else:
            template = "profiles/register.html"
            context = {"form": form}
            return render(request, template, context)


class AcademiaLogin(LoginView):
    template_name = "profiles/login.html"
    authentication_form = AcademiaLoginForm


def content(request):
    template = "profiles/content.html"
    context = {"content_index_active": "active"}
    return render(request, template, context)


def profile_data(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        interests = request.POST.get("interests")
        profile_description = request.POST.get("profile_description")

        profile = Profile.objects.get(user=request.user)
        request.user.username = username
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        profile.interests = interests
        profile.profile_description = profile_description
        profile.save()

        return HttpResponse("printed!")

    else:
        template = "profiles/profile_data.html"
        profile, created = Profile.objects.get_or_create(user=request.user)  # loggear si created
        accepted_cryptos = profile.cryptos_list()
        cryptos_string = ""
        for c in accepted_cryptos:
            cryptos_string += (c.code + ", ")
        if len(cryptos_string) > 2:
            cryptos_string = cryptos_string[:-2]

        context = {"profile_index_active": "active", "underline_pdata": "text-underline",
                   "profile": profile, "accepted_cryptos": accepted_cryptos,
                   "cryptos_string": cryptos_string}
        return render(request, template, context)


def profile_edit_contact(request):
    template = "profiles/profile_edit_contact.html"
    if request.method == "POST":
        post_data = request.POST
        print("post_data: %s" % post_data)

    context = {}
    return render(request, template, context)


def profile_edit_cryptos(request):
    pass


def profile_security(request):
    template = "profiles/profile_security.html"
    context = {"profile_index_active": "active", "underline_psecurity": "text-underline"}
    return render(request, template, context)


def profile_events(request):
    template = "profiles/profile_events.html"
    events = Event.objects.filter(owner=request.user)
    context = {"profile_index_active": "active", "underline_pevents": "text-underline",
               "events": events}
    return render(request, template, context)


def profile_accreditation(request):
    template = "profiles/profile_accreditations.html"
    context = {"profile_index_active": "active", "underline_paccreditation": "text-underline"}
    return render(request, template, context)


def profile_certificates(request):
    template = "profiles/profile_certificates.html"
    context = {"profile_index_active": "active", "underline_pcertificates": "text-underline"}
    return render(request, template, context)


def profile_content(request):
    template = "profiles/profile_content.html"
    context = {"profile_index_active": "active", "underline_pcontent": "text-underline"}
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
