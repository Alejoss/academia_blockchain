from http import HTTPStatus

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

from profiles.utils import AcademiaUserCreationForm, AcademiaLoginForm
from profiles.models import Profile, AcceptedCrypto, ContactMethod
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

        contact_methods = ContactMethod.objects.filter(user=request.user, deleted=False)
        print("contact_methods:%s" % contact_methods)

        context = {"profile_index_active": "active", "underline_pdata": "text-underline",
                   "profile": profile, "accepted_cryptos": accepted_cryptos,
                   "cryptos_string": cryptos_string, "contact_methods": contact_methods}
        return render(request, template, context)


def profile_edit_contact(request):
    template = "profiles/profile_edit_contact.html"

    if request.method == "POST":
        contact_id = request.POST.get("contact_id")
        contact_name = request.POST.get("contact_name")
        contact_url = request.POST.get("contact_url")
        contact_description = request.POST.get("contact_text")

        if int(contact_id) > 0:  # ContactMethod existente
            try:
                obj = ContactMethod.objects.get(id=contact_id)
            except Exception as e:
                return HttpResponse("Contact Method not found", status=404)
            if contact_name == "0":
                # Delete ContactMethod
                obj.deleted = True
                obj.save()
            else:
                obj.name = contact_name
                obj.url_link = contact_url
                obj.description = contact_description
                obj.save()
        else:  # Crear nuevo ContactMethod
            if len(contact_name) > 1:
                new_obj = ContactMethod.objects.create(
                    user=request.user,
                    name=contact_name,
                    url_link=contact_url,
                    description=contact_description
                )
                return HttpResponse("New Contact Method created")

        return HttpResponse("SUCESSS")
    else:
        contact_methods = ContactMethod.objects.filter(user=request.user, deleted=False)
        print("contact_methods: %s" % contact_methods)
        context = {"contact_methods": contact_methods}
        return render(request, template, context)


def profile_edit_cryptos(request):
    template = "profiles/profile_edit_contact.html"

    if request.method == "POST":
        # contact_id = request.POST.get("contact_id")
        # contact_name = request.POST.get("contact_name")
        # contact_url = request.POST.get("contact_url")
        # contact_description = request.POST.get("contact_text")
        #
        # if int(contact_id) > 0:  # ContactMethod existente
        #     try:
        #         obj = ContactMethod.objects.get(id=contact_id)
        #     except Exception as e:
        #         return HttpResponse("Contact Method not found", status=404)
        #     if contact_name == "0":
        #         # Delete ContactMethod
        #         obj.deleted = True
        #         obj.save()
        #     else:
        #         obj.name = contact_name
        #         obj.url_link = contact_url
        #         obj.description = contact_description
        #         obj.save()
        # else:  # Crear nuevo ContactMethod
        #     if len(contact_name) > 1:
        #         new_obj = ContactMethod.objects.create(
        #             name=contact_name,
        #             url_link=contact_url,
        #             description=contact_description
        #         )
        #         new_obj.user.add(request.user)
        #         return HttpResponse("New Contact Method created")

        return HttpResponse("SUCESSS")
    else:
        accepted_cryptos = AcceptedCrypto.objects.filter(user=request.user)
        print("accepted_cryptos: %s" % accepted_cryptos)
        context = {"accepted_cryptos": accepted_cryptos}
        return render(request, template, context)


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
