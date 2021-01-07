from http import HTTPStatus
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse

from profiles.utils import AcademiaUserCreationForm, AcademiaLoginForm, ProfilePictureForm, \
    get_cryptos_string, academia_blockchain_timezones
from profiles.models import Profile, AcceptedCrypto, ContactMethod, CryptoCurrency
from courses.models import Event, Bookmark, CertificateRequest, Certificate

logger = logging.getLogger(__name__)


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

            # Crear Accepted Cryptos por default
            bitcoin, created = CryptoCurrency.objects.get_or_create(name="Bitcoin", code="BTC")
            ether, created = CryptoCurrency.objects.get_or_create(name="Ether", code="ETH")
            monero, created = CryptoCurrency.objects.get_or_create(name="Monero", code="XMR")

            AcceptedCrypto.objects.create(user=new_user, crypto=bitcoin)
            AcceptedCrypto.objects.create(user=new_user, crypto=ether)
            AcceptedCrypto.objects.create(user=new_user, crypto=monero)

            login(request, new_user)

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


@login_required
def profile_data(request):
    logging.info("INFO PROFILE DATA!!")
    logging.debug("DEBUG PROFILE DATA!!")
    logging.warning("WARNING PROFILE DATA!!")
    logging.error("ERROR PROFILE DATA!!")
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        time_zone = request.POST.get("time_zone")
        interests = request.POST.get("interests")
        profile_description = request.POST.get("profile_description")

        request.user.email = email
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        profile = Profile.objects.get(user=request.user)
        profile.timezone = time_zone
        profile.interests = interests
        profile.profile_description = profile_description
        profile.save()

        return redirect("profile_data")

    else:
        template = "profiles/profile_data.html"
        profile, created = Profile.objects.get_or_create(user=request.user)  # loggear si created
        cryptos_string = get_cryptos_string(profile)

        contact_methods = ContactMethod.objects.filter(user=request.user, deleted=False)

        profile_picture_form = ProfilePictureForm()

        context = {"profile_index_active": "active", "underline_data": "text-underline",
                   "profile": profile, "academia_blockchain_timezones": academia_blockchain_timezones(),
                   "cryptos_string": cryptos_string, "contact_methods": contact_methods,
                   "profile_picture_form": profile_picture_form}
        return render(request, template, context)


@login_required
def user_profile(request, profile_id):
    template = "profiles/user_profile.html"
    profile = get_object_or_404(Profile, user__id=profile_id)

    contact_methods = ContactMethod.objects.filter(user=profile.user, deleted=False)
    cryptos_string = get_cryptos_string(profile)
    events = Event.objects.filter(owner=profile.user)

    context = {"profile": profile, "events": events, "contact_methods": contact_methods,
               "cryptos_string": cryptos_string}
    return render(request, template, context)


@login_required
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
        context = {"contact_methods": contact_methods}
        return render(request, template, context)


@login_required
def profile_edit_picture(request):
    if request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
        return redirect("profile_data")
    else:
        return HttpResponse(status=400)


@login_required
def profile_edit_cryptos(request):
    template = "profiles/profile_edit_cryptos.html"

    if request.method == "POST":
        crypto_id = request.POST.get("crypto_id")
        crypto_name = request.POST.get("crypto_name")
        crypto_code = request.POST.get("crypto_code")
        crypto_address = request.POST.get("crypto_address")

        if int(crypto_id) > 0:  # AcceptedCrypto existente
            try:
                obj = AcceptedCrypto.objects.get(id=crypto_id)
            except Exception as e:
                return HttpResponse("Accepted Crypto not found", status=404)
            if crypto_name == "0":
                # Remove Accepted Crypto
                obj.deleted = True
                obj.save()
            else:
                if CryptoCurrency.objects.filter(name=crypto_name).exists():
                    crypto_obj = CryptoCurrency.objects.get(name=crypto_name)
                    obj.crypto = crypto_obj
                else:
                    # Crear una nueva criptomoneda
                    new_crypto = CryptoCurrency.objects.create(name=crypto_name,
                                                               code=crypto_code)
                    obj.crypto = new_crypto
                obj.address = crypto_address
                obj.save()

        else:  # Crear nuevo AcceptedCrypto
            if len(crypto_name) > 1:
                if CryptoCurrency.objects.filter(name=crypto_name).exists():
                    crypto_obj = CryptoCurrency.objects.get(name=crypto_name)
                else:
                    # Crear una nueva criptomoneda
                    crypto_obj = CryptoCurrency.objects.create(name=crypto_name,
                                                               code=crypto_code)

                AcceptedCrypto.objects.create(
                    user=request.user,
                    crypto=crypto_obj,
                    address=crypto_address
                )
                return HttpResponse("New Contact Method created")

        return HttpResponse("SUCESSS")
    else:
        accepted_cryptos = AcceptedCrypto.objects.filter(user=request.user, deleted=False)
        context = {"accepted_cryptos": accepted_cryptos}
        return render(request, template, context)


@login_required
def profile_events(request):
    template = "profiles/profile_events.html"
    events = Event.objects.filter(owner=request.user, deleted=False)
    certificate_requests = CertificateRequest.objects.filter(event__owner=request.user, deleted=False,
                                                             accepted__isnull=True)
    context = {"profile_index_active": "active", "underline_events": "text-underline",
               "events": events, "certificate_requests": certificate_requests}
    return render(request, template, context)


@login_required
def profile_certificates(request):
    template = "profiles/profile_certificates.html"
    certificates = Certificate.objects.filter(user=request.user)
    context = {"profile_index_active": "active", "underline_certificates": "text-underline",
               "certificates": certificates}
    return render(request, template, context)

# TODO
# The URL could be /certificate_preview/${transactionId}
# Then, the backend searchs for the transaction in the blockchain and with that data 
# create and send the certificate_data in the context. 
# Suggestion: certificate_data fields could be: graduate, title, author, description, author-address, date and tx-id
# Suggestion: maybe we could add a boolean such as isTxIdValid
# to know if frontend should show a certificate or 404.
# Finally, consume that values in frontend as variables.
@login_required
def certificate_preview(request):
    template = "profiles/certificate_preview.html"
    context = {"certificate_data": ""}
    return render(request, template, context)

@login_required
def profile_cert_requests(request):
    template = "profiles/profile_cert_requests.html"
    cert_requests = CertificateRequest.objects.filter(event__owner=request.user, accepted__isnull=True,
                                                      deleted=False).order_by("event")
    cert_requests_rejected = CertificateRequest.objects.filter(event__owner=request.user, accepted=False,
                                                               deleted=False).order_by("event")
    context = {"cert_requests": cert_requests, "cert_requests_rejected": cert_requests_rejected}
    return render(request, template, context)


@login_required
def profile_bookmarks(request):
    template = "profiles/profile_bookmarks.html"
    bookmarks = []
    bookmarked_events = Bookmark.objects.filter(user=request.user, deleted=False)
    for b in bookmarked_events:
        certificate_request = None
        if CertificateRequest.objects.filter(user=request.user, event=b.event).exists():
            certificate_request = CertificateRequest.objects.get(user=request.user, event=b.event)
        bookmarks.append([b, certificate_request])

    context = {"profile_index_active": "active", "underline_bookmarks": "text-underline",
               "bookmarks": bookmarks}
    return render(request, template, context)


@login_required
def profile_content(request):
    template = "profiles/profile_content.html"
    context = {"profile_index_active": "active", "underline_content": "text-underline"}
    return render(request, template, context)


@login_required
def profile_security(request):
    template = "profiles/profile_security.html"
    context = {"profile_index_active": "active", "underline_security": "text-underline"}
    return render(request, template, context)


def api_create_profile(request):
    if request.is_ajax() and request.method == "POST":
        template = "profiles/create_profile_succesfull.html"
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username, email, password)
        return render(request, template, {"user": user})
    else:
        return HttpResponse(status=HTTPStatus.FORBIDDEN)
