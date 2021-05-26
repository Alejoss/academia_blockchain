from http import HTTPStatus
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from profiles.utils import AcademiaUserCreationForm, AcademiaLoginForm, ProfilePictureForm, \
    get_cryptos_string, academia_blockchain_timezones, send_email_message, AcademiaPasswordResetForm,\
    AcademiaSetPasswordForm, send_confirmation_email

from profiles.models import Profile, AcceptedCrypto, ContactMethod, CryptoCurrency
from courses.models import Event, Bookmark, CertificateRequest, Certificate

logger = logging.getLogger('app_logger')


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
            logger.info("new_user: %s" % new_user.username)

            # Crear perfil de usuario
            new_profile = Profile.objects.create(user=new_user)
            logger.info("new_profile: %s" % new_profile)

            # Crear Accepted Cryptos por default
            bitcoin, created = CryptoCurrency.objects.get_or_create(name="Bitcoin", code="BTC")
            ether, created = CryptoCurrency.objects.get_or_create(name="Ethereum", code="ETH")
            monero, created = CryptoCurrency.objects.get_or_create(name="Monero", code="XMR")

            user_bitcoin = AcceptedCrypto.objects.create(user=new_user, crypto=bitcoin)
            user_ether = AcceptedCrypto.objects.create(user=new_user, crypto=ether)
            user_monero = AcceptedCrypto.objects.create(user=new_user, crypto=monero)

            logger.info("user_bitcoin: %s" % user_bitcoin)
            logger.info("user_ether: %s" % user_ether)
            logger.info("user_monero: %s" % user_monero)

            login(request, new_user)
            email = form.cleaned_data['email']
            # Enviar email de confirmacion
            send_confirmation_email(request, new_user, email)

            template = "profiles/profile_data.html"
            context = {'new_profile': new_profile}
            return render(request, template, context)
        else:
            template = "profiles/register.html"
            context = {"form": form}
            return render(request, template, context)


def activate_account(request, uid, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        logger.debug("uid: %s" % uid)
        user = User.objects.get(pk=uid)
        check_token = PasswordResetTokenGenerator().check_token(user, token)
        logger.debug("check_token: %s" % check_token)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        check_token = False
    if user is not None and check_token:
        profile = get_object_or_404(Profile, user=user)
        profile.email_confirmed = True
        profile.save()
        login(request, user)
        template = "profiles/account_activate_complete.html"
        context = {}
        return render(request, template, context)
    else:
        return HttpResponse('Activation link is invalid!')


class AcademiaLogin(LoginView):
    template_name = "profiles/login.html"
    authentication_form = AcademiaLoginForm


class AcademiaPasswordResetView(PasswordResetView):
    email_template_name = "profiles/password_reset_email.html"
    template_name = 'profiles/password_reset_form.html'
    form_class = AcademiaPasswordResetForm


class AcademiaPasswordResetDoneView(PasswordResetDoneView):
    template_name = "profiles/email_sent.html"


class AcademiaPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "profiles/password_reset_confirm.html"
    form_class = AcademiaSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class AcademiaPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "profiles/password_reset_complete.html"


def resend_activation_email(request):
    user_email = request.user.email
    if user_email:
        logger.debug("user_email: %s" % user_email)
        send_confirmation_email(request, request.user, user_email)
        template = "profiles/email_sent.html"
        context = {}
        return render(request, template, context)
    else:
        return HttpResponse("email not found")


def content(request):
    template = "profiles/content.html"
    context = {"content_index_active": "active"}
    return render(request, template, context)


@login_required
def profile_data(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        time_zone = request.POST.get("time_zone")
        interests = request.POST.get("interests")
        profile_description = request.POST.get("profile_description")

        logger.info("email: %s" % email)
        logger.info("first_name: %s" % first_name)
        logger.info("last_name: %s" % last_name)
        logger.info("time_zone: %s" % time_zone)
        logger.info("interests: %s" % interests)
        logger.info("profile_description: %s" % profile_description)

        request.user.email = email
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        profile = Profile.objects.get(user=request.user)
        logger.info("profile: %s" % profile)

        profile.timezone = time_zone
        profile.interests = interests
        profile.profile_description = profile_description
        profile.save()

        return redirect("profile_data")

    else:
        template = "profiles/profile_data.html"
        profile, created = Profile.objects.get_or_create(user=request.user)
        if created:
            logger.warning("created: %s" % created)
        logger.info("profile: %s" % profile)

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
    logger.info("contact_methods: %s" % contact_methods)
    cryptos_string = get_cryptos_string(profile)
    events = Event.objects.filter(owner=profile.user)
    logger.info("events: %s" % events)

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

        logger.info("contact_id: %s" % contact_id)
        logger.info("contact_name: %s" % contact_name)
        logger.info("contact_url: %s" % contact_url)
        logger.info("contact_description: %s" % contact_description)

        if int(contact_id) > 0:  # ContactMethod existente
            try:
                obj = ContactMethod.objects.get(id=contact_id)
            except Exception as e:
                logger.warning("contact_id not found: %s" % contact_id)
                return HttpResponse("Contact Method not found", status=404)
            if contact_name == "0":
                # Delete ContactMethod - Esto puede mejorar
                logger.info("delete contact_method")
                obj.deleted = True
                obj.save()
            else:
                obj.name = contact_name
                obj.url_link = contact_url
                obj.description = contact_description
                obj.save()
        else:  # Crear nuevo ContactMethod
            if len(contact_name) > 1:
                new_contact_method = ContactMethod.objects.create(
                    user=request.user,
                    name=contact_name,
                    url_link=contact_url,
                    description=contact_description
                )
                logger.info("new_contact_method: %s" % new_contact_method)
                return HttpResponse("New Contact Method created")

        return HttpResponse("SUCESSS")
    else:
        contact_methods = ContactMethod.objects.filter(user=request.user, deleted=False)
        logger.info("contact_methods: %s" % contact_methods)
        context = {"contact_methods": contact_methods}
        return render(request, template, context)


@login_required
def profile_edit_picture(request):
    if request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        logger.info("user_profile: %s" % user_profile)

        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
        else:
            logger.warning(form.errors)
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

        logger.info("crypto_id: %s" % crypto_id)
        logger.info("crypto_name: %s" % crypto_name)
        logger.info("crypto_code: %s" % crypto_code)
        logger.info("crypto_address: %s" % crypto_address)

        if int(crypto_id) > 0:  # AcceptedCrypto existente
            try:
                obj = AcceptedCrypto.objects.get(id=crypto_id)
            except Exception as e:
                logger.warning("accepted_crypto not found: %s" % crypto_id)
                return HttpResponse("Accepted Crypto not found", status=404)
            if crypto_name == "0":
                # Remove Accepted Crypto
                logger.info("delete accepted_crypto: %s" % crypto_id)
                obj.deleted = True
                obj.save()
            else:
                if CryptoCurrency.objects.filter(name=crypto_name).exists():
                    crypto_obj = CryptoCurrency.objects.get(name=crypto_name)
                    logger.info("crypto_obj: %s" % crypto_obj)
                    obj.crypto = crypto_obj
                else:
                    # Crear una nueva criptomoneda
                    new_crypto = CryptoCurrency.objects.create(name=crypto_name,
                                                               code=crypto_code)
                    logger.info("new_crypto: %s" % new_crypto)
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
                logger.info("crypto_obj: %s" % crypto_obj)

                new_accepted_crypto = AcceptedCrypto.objects.create(
                    user=request.user,
                    crypto=crypto_obj,
                    address=crypto_address
                )
                logger.info("new_accepted_crypto: %s" % new_accepted_crypto)
                return HttpResponse("New Contact Method created")

        return HttpResponse("SUCESSS")
    else:
        accepted_cryptos = AcceptedCrypto.objects.filter(user=request.user, deleted=False)
        logger.info("accepted_cryptos: %s" % accepted_cryptos)

        context = {"accepted_cryptos": accepted_cryptos}
        return render(request, template, context)


@login_required
def profile_events(request):
    template = "profiles/profile_events.html"
    events = Event.objects.filter(owner=request.user, deleted=False)
    logger.info("events: %s" % events)

    certificate_requests = CertificateRequest.objects.filter(event__owner=request.user, deleted=False,
                                                             accepted__isnull=True)
    logger.info("certificate_requests: %s" % certificate_requests)

    context = {"profile_index_active": "active", "underline_events": "text-underline",
               "events": events, "certificate_requests": certificate_requests}
    return render(request, template, context)


@login_required
def profile_certificates(request):
    template = "profiles/profile_certificates.html"
    certificates = Certificate.objects.filter(user=request.user)
    logger.info("certificates: %s" % certificates)

    courses_certificates = Certificate.objects.filter(event__owner=request.user)  # certificates awarded by user

    context = {"profile_index_active": "active", "underline_certificates": "text-underline",
               "certificates": certificates, "courses_certificates": courses_certificates}
    return render(request, template, context)


@login_required
def profile_cert_requests(request):
    template = "profiles/profile_cert_requests.html"
    cert_requests = CertificateRequest.objects.filter(event__owner=request.user, accepted__isnull=True,
                                                      deleted=False).order_by("event")
    logger.info("cert_requests: %s" % cert_requests)

    cert_requests_rejected = CertificateRequest.objects.filter(event__owner=request.user, accepted=False,
                                                               deleted=False).order_by("event")
    logger.info("cert_requests_rejected: %s" % cert_requests_rejected)
    context = {"cert_requests": cert_requests, "cert_requests_rejected": cert_requests_rejected}
    return render(request, template, context)


@login_required
def profile_bookmarks(request):
    template = "profiles/profile_bookmarks.html"
    bookmarks = []
    bookmarked_events = Bookmark.objects.filter(user=request.user, deleted=False)
    logger.info("bookmarked_events: %s" % bookmarked_events)

    for b in bookmarked_events:
        certificate_request = None
        if CertificateRequest.objects.filter(user=request.user, event=b.event).exists():
            certificate_request = CertificateRequest.objects.get(user=request.user, event=b.event)
        bookmarks.append([b, certificate_request])

    logger.info("bookmarks: %s" % bookmarks)

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
