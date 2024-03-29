from http import HTTPStatus
import pytz
import logging
import json
from pycoingecko import CoinGeckoAPI
from http import HTTPStatus
from datetime import datetime
from hashlib import sha256
import requests
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
from urllib.request import urlopen

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import is_aware
from django.contrib.auth import get_user
from django.http import HttpResponse

from courses.models import Event, ConnectionPlatform, Bookmark, CertificateRequest, Certificate, Comment
from profiles.models import ContactMethod, AcceptedCrypto, Profile
from profiles.utils import academia_blockchain_timezones
from courses.utils import get_event_data_request
from star_ratings.models import Rating
from taggit.models import Tag

logger = logging.getLogger('app_logger')

"""
HTML RENDERS
"""


def event_index(request):
    template = "courses/events.html"
    events = Event.objects.filter(deleted=False)
    tags = Tag.objects.all()
    logger.info("events: %s" % events)
    context = {"events": events, "event_index_active": "active", "tags": tags}
    return render(request, template, context)


def about(request):
    template = "courses/about.html"
    context = {"info_index_active": "active"}
    return render(request, template, context)


def descentralize_education(request):
    template = "courses/descentralize_education.html"
    context = {"info_index_active": "active"}
    return render(request, template, context)


def events_tag(request, tag_id):
    template = "courses/events_tag.html"
    tag = get_object_or_404(Tag, id=tag_id)
    tags = Tag.objects.all()
    events = Event.objects.filter(tags__name__in=[tag.name])
    context = {"events": events, "event_index_active": "active", "tags": tags, "tag": tag}
    return render(request, template, context)


def events_all(request):
    template = "courses/events_all.html"
    events = Event.objects.all()
    tags = Tag.objects.all()
    context = {"events": events, "event_index_active": "active", "tags": tags}
    return render(request, template, context)


def event_search(request):
    template = "courses/events_result.html"
    if request.method == "POST":
        query = request.POST.get("q")
        logger.info("query: %s" % query)

        events = Event.objects.filter(title__icontains=query)

        logger.info("events: %s" % events)
        context = {"events": events, "query": query}
        return render(request, template, context)
    else:
        return HttpResponse(status=400)


def event_detail(request, event_id):
    template = "courses/event_detail.html"
    event = get_object_or_404(Event, id=event_id)
    logger.info("event: %s" % event)

    contact_methods = ContactMethod.objects.filter(user=event.owner, deleted=False)
    accepted_cryptos = AcceptedCrypto.objects.filter(user=event.owner, deleted=False)
    preferred_cryptos = coins_value(accepted_cryptos, event)
    # llama al API CoinGeko y devuelve una lista con las monedas aceptadas por el usuario y sus valores.
    owner_profile = Profile.objects.get(user=event.owner)

    logger.info("contact_methods: %s" % contact_methods)
    logger.info("preferred_cryptos: %s" % preferred_cryptos)

    academia_blockchain_timezones()

    event_user_timezone = None
    logged_user_profile = None
    event_is_bookmarked = False
    user_certificate_request = None
    if request.user.is_authenticated:
        logged_user_profile = Profile.objects.get(user=request.user)
        try:
            user_timezone = pytz.timezone("America/Guayaquil")
            event_user_timezone = event.date_start.astimezone(user_timezone)
        except Exception as e:
            pass

        event_is_bookmarked = Bookmark.objects.filter(event=event, user=request.user, deleted=False).exists()
        if CertificateRequest.objects.filter(event=event, user=request.user).exists():
            user_certificate_request = CertificateRequest.objects.get(event=event, user=request.user)

    logger.info("event_user_timezone: %s" % event_user_timezone)
    logger.info("logged_user_profile: %s" % logged_user_profile)
    logger.info("event_is_bookmarked: %s" % event_is_bookmarked)

    is_event_owner = (event.owner == request.user)
    certificate_requests = CertificateRequest.objects.none()

    logger.info("is_event_owner: %s" % is_event_owner)
    if is_event_owner:
        certificate_requests = CertificateRequest.objects.filter(event=event, state="PENDING")
        logger.info("certificate_requests: %s" % certificate_requests)

    comments = Comment.objects.filter(event=event, deleted=False)
    rating = Rating.objects.for_instance(event)
    has_certificate = False
    if request.user.is_authenticated:
        has_certificate = Certificate.objects.filter(event=event, user=request.user).exists()
    logger.info("has_certificate: %s" % has_certificate)
    logger.info("user_certificate_request: %s" % user_certificate_request)

    context = {"event": event, "contact_methods": contact_methods, "accepted_cryptos": accepted_cryptos,
               "owner_profile": owner_profile, "event_user_timezone": event_user_timezone,
               "logged_user_profile": logged_user_profile, "event_is_bookmarked": event_is_bookmarked,
               "is_event_owner": is_event_owner, "user_certificate_request": user_certificate_request,
               "certificate_requests": certificate_requests, "comments": comments, 'rating': rating,
               'lack_certificate': not has_certificate, "preferred_cryptos": preferred_cryptos}
    return render(request, template, context)


def event_recorded_online(request):
    template = "courses/event_recorded_online.html"
    context = {"event_index_active": "active"}
    return render(request, template, context)


def event_recurrent_localized(request):
    template = "courses/event_recurrent_localized.html"
    context = {"event_index_active": "active"}
    return render(request, template, context)


def event_singular_online(request):
    template = "courses/event_singular_online.html"
    context = {"event_index_active": "active"}
    return render(request, template, context)


@login_required
def event_create(request):
    if request.method == "GET":
        template = "courses/event_create.html"
        platforms = ConnectionPlatform.objects.filter(deleted=False)
        profile = Profile.objects.get(user=request.user)
        logger.info("platforms: %s" % platforms)
        logger.info("profile.email_confirmed: %s" % profile.email_confirmed)
        user_contact_methods = ContactMethod.objects.filter(user=request.user)

        context = {"event_index_active": "active", "platforms": platforms, "profile": profile,
                   "user_contact_methods": user_contact_methods}
        return render(request, template, context)

    elif request.method == "POST":
        event_data = get_event_data_request(request)

        created_event = Event.objects.create(
            event_type=event_data['event_type'],
            is_recurrent=event_data['event_recurrent'],
            owner=request.user,
            title=event_data['title'],
            description=event_data['description'],
            platform=event_data['platform'],
            other_platform=event_data['other_platform'],
            date_start=event_data['date_start'],
            date_end=event_data['date_end'],
            date_recorded=event_data['record_date'],
            schedule_description=event_data['schedule_description']
        )

        profile = Profile.objects.get(user=request.user)
        profile.is_teacher = True
        profile.save()

        # Guardar imagen
        if "event_picture" in request.FILES:
            event_picture = request.FILES['event_picture']
            logger.info("event_picture: %s" % event_picture)
            created_event.image.save(event_picture.name, event_picture)

        # Sumar Tags
        for tag in event_data['tags']:
            logger.info("tag_added: %s" % tag)
            created_event.tags.add(tag)

        return redirect("event_detail", event_id=created_event.id)


@login_required
def event_edit(request, event_id):
    if request.method == "GET":
        template = "courses/event_edit.html"
        event = get_object_or_404(Event, id=event_id)
        logger.info("event: %s" % event)
        platforms = ConnectionPlatform.objects.filter(deleted=False)
        user_contact_methods = ContactMethod.objects.filter(user=event.owner)
        event_tags = [e.name for e in event.tags.all()]
        logger.info("platforms: %s" % platforms)
        logger.info("user_contact_methods: %s" % user_contact_methods)

        context = {"event": event, "platforms": platforms, "user_contact_methods": user_contact_methods,
                   "event_tags": json.dumps(event_tags)}
        return render(request, template, context)

    elif request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        event_data = get_event_data_request(request)

        event.event_type = event_data['event_type']
        event.is_recurrent = event_data['event_recurrent']
        event.owner = request.user
        event.title = event_data['title']
        event.description = event_data['description']
        event.platform = event_data['platform']
        event.other_platform = event_data['other_platform']
        event.date_start = event_data['date_start']
        event.date_end = event_data['date_end']
        event.date_recorded = event_data['record_date']
        event.schedule_description = event_data['schedule_description']
        event.save()

        # Guardar imagen
        if "event_picture" in request.FILES:
            event_picture = request.FILES['event_picture']
            logger.info("event_picture: %s" % event_picture)
            event.image.save(event_picture.name, event_picture)

        # Actualizar tags
        event_tags = [e.name for e in event.tags.all()]
        for tag in event_data['tags']:
            if tag not in event_tags:
                event.tags.add(tag.strip())
                logger.info("new_tag: %s" % tag)
        for existing_tag in event_tags:
            if existing_tag not in event_data['tags']:
                event.tags.remove(existing_tag)
                logger.info("remove_tag: %s" % existing_tag)

        return redirect("event_detail", event_id=event.id)


@login_required
def event_delete(request, event_id):
    deleted_event = get_object_or_404(Event, id=event_id)
    logger.info("deleted_event: %s" % deleted_event)
    if not request.user == deleted_event.owner:
        return HttpResponse(status=403)

    deleted_event.deleted = True
    deleted_event.save()
    return redirect("profile_events")


@login_required
def event_comment(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        comment_text = request.POST.get("comment_text", None)
        logger.info("event: %s" % event)
        logger.info("comment_text: %s" % comment_text)
        if comment_text:
            comment = Comment.objects.create(
                event=event,
                user=request.user,
                text=comment_text
            )
            logger.info("comment: %s" % comment)
        return redirect("event_detail", event_id=event.id)
    else:
        return HttpResponse(status=400)


def certificate_preview(request, cert_id):
    template = "courses/certificate_preview.html"

    certificate = get_object_or_404(Certificate, id=cert_id)

    certificate_image_base = requests.get("https://criptolibertad.s3.us-west-2.amazonaws.com/img/base_cert.jpg")
    img = Image.open(BytesIO(certificate_image_base.content))

    font_title_event = ImageFont.truetype(
        urlopen("https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-Medium.ttf"), size=70)
    font_title_event_medium = ImageFont.truetype(
        urlopen("https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-Medium.ttf"), size=38)


    font_owner_event = ImageFont.truetype(
        urlopen("https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-LightItalic.ttf"), size=38)
    font_owner_certificate = ImageFont.truetype(
        urlopen("https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-Black.ttf"), size=40)
    font_date = ImageFont.truetype(
        urlopen("https://criptolibertad.s3.us-west-2.amazonaws.com/img/fonts/Roboto-LightItalic.ttf"), size=24)

    img_draw = ImageDraw.Draw(img)

    # titulo del evento
    if len(certificate.event.title) < 33:
        img_draw.multiline_text((450, 350), certificate.event.title, font=font_title_event, fill=(96, 96, 96))
    else:
        img_draw.multiline_text((450, 350), certificate.event.title, font=font_title_event_medium, fill=(96, 96, 96))


    # creador del evento
    img_draw.multiline_text((545, 505), certificate.event.owner.username, font=font_owner_event, fill=(96, 96, 96))

    # nombre de usuario para el certificado
    img_draw.multiline_text((310, 800), certificate.user.username, font=font_owner_certificate,
                            fill=(96, 96, 96))

    # fecha
    img_draw.multiline_text((310, 935), certificate.date_created.strftime("%d %b %Y"), font=font_date,
                            fill=(96, 96, 96))

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    print("img: %s" % img)
    img_bytes = buffered.getvalue()  # bytes
    print("img_bytes: %s" % img_bytes)
    img_base64 = base64.b64encode(img_bytes)  # Base64 - encoded bytes
    print("img_base64: %s" % img_base64)
    img_str = img_base64.decode('utf-8')
    print("img_str: %s" % img_str)

    context = {"img_str": img_str}
    return render(request, template, context)


def send_cert_blockchain(request, cert_id):
    template = "courses/send_cert_blockchain.html"
    certificate = get_object_or_404(Certificate, id=cert_id)
    cert_text = (certificate.user.username + certificate.user.first_name + certificate.user.last_name +
                 certificate.event.title + certificate.event.owner.username).encode("utf8")
    logger.info("cert_text: %s" % cert_text)
    cert_hash = sha256(cert_text)
    logger.info("cert_hash: %s" % cert_hash)

    context = {"certificate": certificate, "cert_text": cert_text, "cert_hash": cert_hash}
    return render(request, template, context)


def add_cert_hash(request, cert_id):
    if request.method == "POST":
        pass
    else:
        pass


"""
API CALLS
"""


@login_required
def event_bookmark(request, event_id):
    if request.is_ajax() and request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        logger.info("event: %s" % event)
        if Bookmark.objects.filter(event=event, user=request.user, deleted=False).exists():
            return HttpResponse(status=200)
        else:
            if Bookmark.objects.filter(event=event, user=request.user, deleted=True).exists():
                bookmark = Bookmark.objects.get(event=event, user=request.user, deleted=True)
                logger.info("bookmark: %s" % bookmark)
                bookmark.deleted = False
                bookmark.save()
            else:
                Bookmark.objects.create(event=event, user=request.user)
            return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


@login_required
def remove_bookmark(request, event_id):
    if request.is_ajax() and request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        if Bookmark.objects.filter(event=event, user=request.user, deleted=False).exists():
            bookmark = Bookmark.objects.get(user=request.user, event=event, deleted=False)
            logger.info("bookmark: %s" % bookmark)
            bookmark.deleted = True
            bookmark.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

    else:
        return HttpResponse(status=403)


def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    cert_data = {
        "id": certificate.id,
        "username": certificate.user.username,
        "first_name": certificate.user.first_name,
        "last_name": certificate.user.last_name,
        "cert_date": certificate.date_created,
        "event_title": certificate.event.title,
        "event_description": certificate.event.description,
        "event_owner_username": certificate.event.owner.username,
        "event_owner_first_name": certificate.event.owner.first_name,
        "event_owner_last_name": certificate.event.owner.last_name,
    }
    return JsonResponse(cert_data)


@login_required
def request_certificate(request, event_id):
    if request.is_ajax() and request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        logger.info("event: %s" % event)
        if CertificateRequest.objects.filter(event=event, user=request.user, state="DELETED").exists():
            certificate_request = CertificateRequest.objects.get(event=event, user=request.user, state="DELETED")
            logger.info("certificate_request: %s" % certificate_request)
            certificate_request.state = "PENDING"
            certificate_request.save()
        else:
            CertificateRequest.objects.create(event=event, user=request.user, state="PENDING")
        return HttpResponse(status=201)

    else:
        return HttpResponse(status=403)


@login_required
def cancel_cert_request(request, cert_request_id):
    if request.is_ajax() and request.method == "POST":
        certificate_request = get_object_or_404(CertificateRequest, id=cert_request_id)
        logger.info("certificate_request: %s" % certificate_request)
        if request.user == certificate_request.user:
            if Certificate.objects.filter(event=certificate_request.event, user=certificate_request.user).exists():
                logger.warning("Intento de cancelar certificado existente: %s" % certificate_request.id)
                certificate_request.state = "ACCEPTED"
                # si existe el certificado, el state del certificate request debe ser ACCEPTED
                certificate_request.save()
            else:
                certificate_request.state = "DELETED"
                certificate_request.save()
            return HttpResponse(status=201)
        else:
            logger.warning("request.user: %s" % request.user)
            logger.warning("certificate_request.event.owner: %s" % certificate_request.event.owner)
            logger.warning("request.user =! certificate_request.event.owner")
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)


@login_required
def accept_cert_request(request, cert_request_id):
    if request.is_ajax() and request.method == "POST":
        certificate_request = get_object_or_404(CertificateRequest, id=cert_request_id)
        logger.info("certificate_request: %s" % certificate_request)
        if request.user == certificate_request.event.owner:
            if Certificate.objects.filter(event=certificate_request.event, user=certificate_request.user).exists():
                logger.warning("certificate ya existe")
            else:
                new_cert = Certificate.objects.create(event=certificate_request.event, user=certificate_request.user)
                logger.info("new_cert: %s" % new_cert)
            certificate_request.state = "ACCEPTED"
            certificate_request.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)


def reject_cert_request(request, cert_request_id):
    if request.is_ajax() and request.method == "POST":
        certificate_request = get_object_or_404(CertificateRequest, id=cert_request_id)
        logger.info("certificate_request: %s" % certificate_request)
        if request.user == certificate_request.event.owner:
            if Certificate.objects.filter(event=certificate_request.event, user=certificate_request.user).exists():
                logger.warning("Intento de rechazar certificado existente: %s" % certificate_request.id)
                certificate_request.state = "ACCEPTED"  # si existe el certificado, el state debe ser ACCEPTED
                certificate_request.save()
                pass  # No puede rechazar si ya existe el certificado
            else:
                certificate_request.state = "REJECTED"
                certificate_request.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)


def restore_cert_request(request, cert_request_id):
    if request.is_ajax() and request.method == "POST":
        certificate_request = get_object_or_404(CertificateRequest, id=cert_request_id)
        logger.info("certificate_request: %s" % certificate_request)
        if request.user == certificate_request.event.owner:
            if Certificate.objects.filter(event=certificate_request.event, user=certificate_request.user).exists():
                logger.warning("Intento de restaurar certificado existente: %s" % certificate_request.id)
                pass  # No puede rechazar si ya existe el certificado
            else:
                certificate_request.state = "PENDING"
                certificate_request.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)


# API coingeko
def coins_value(accepted_cryptos, event):
    if (event.reference_price != 0):
        ways_to_pay = []
        for c in accepted_cryptos:  # se crea una lista de las monedas aceptadas.
            ways_to_pay.append(c.crypto.name.lower())

        try:
            coins_request = CoinGeckoAPI().get_coins_markets(ids=ways_to_pay,
                                                             vs_currency='usd')  # solicita la informacion de las monedas aceptadas.
            crypto_info = []
            for coin in coins_request:  # se crea una lista con los valores de las monedas
                event_reference_price_crypto = event.reference_price / coin["current_price"]
                crypto_info.append(
                    {"id": coin["id"], "image": coin["image"], "symbol": coin["symbol"], "name": coin["name"],
                     "current_price": coin["current_price"],
                     "event_reference_price_crypto": event_reference_price_crypto})
            return crypto_info
        except Exception as e:
            print(e)
            print('No es posible conectarse al API de coingecko en este momento')
            return [{"id": "error al conectar el API", "image": "", "symbol": "ERROR", "name": "error",
                     "current_price": "error al conectar el API",
                     "event_reference_price_crypto": "error al conectar el API"}]
