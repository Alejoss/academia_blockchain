from http import HTTPStatus
import pytz
import json
from http import HTTPStatus
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import is_aware
from django.contrib.auth import get_user
from django.http import HttpResponse

from courses.models import Event, ConnectionPlatform, Bookmark, CertificateRequest, Certificate
from profiles.models import ContactMethod, AcceptedCrypto, Profile
from profiles.utils import academia_blockchain_timezones

"""
HTML RENDERS
"""


def event_index(request):
    template = "courses/events.html"
    events = Event.objects.all()
    print("events:%s" % events)
    for event in events:
        print(event.event_type)
    context = {"events": events, "event_index_active": "active"}
    return render(request, template, context)


def event_detail(request, event_id):
    template = "courses/event_detail.html"
    event = get_object_or_404(Event, id=event_id)

    contact_methods = ContactMethod.objects.filter(user=event.owner, deleted=False)
    accepted_cryptos = AcceptedCrypto.objects.filter(user=event.owner, deleted=False)
    owner_profile = Profile.objects.get(user=event.owner)

    academia_blockchain_timezones()

    event_user_timezone = None
    logged_user_profile = None
    event_is_bookmarked = False
    if request.user.is_authenticated:
        logged_user_profile = Profile.objects.get(user=request.user)
        try:
            # TODO mostrar los tiempos del evento en la hora del visitante
            user_timezone = pytz.timezone("America/Guayaquil")
            event_user_timezone = event.date_start.astimezone(user_timezone)
        except Exception as e:
            print("ERROR: %s" % e)
        event_is_bookmarked = Bookmark.objects.filter(event=event, user=request.user, deleted=False).exists()

    is_event_owner = (event.owner == request.user)
    event_bookmarks = Bookmark.objects.none()
    certificate_requests = CertificateRequest.objects.none()
    if is_event_owner:
        event_bookmarks = Bookmark.objects.filter(event=event, deleted=False)
        certificate_requests = CertificateRequest.objects.filter(event=event, deleted=False)

    context = {"event": event, "contact_methods": contact_methods, "accepted_cryptos": accepted_cryptos,
               "owner_profile": owner_profile, "event_user_timezone": event_user_timezone,
               "logged_user_profile": logged_user_profile, "event_is_bookmarked": event_is_bookmarked,
               "is_event_owner": is_event_owner, "event_bookmarks": event_bookmarks,
               "certificate_requests": certificate_requests}
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
    # TODO este form y el de edit podria utilizar el mismo codigo y django forms
    if request.method == "GET":
        template = "courses/event_create.html"
        platforms = ConnectionPlatform.objects.filter(deleted=False)

        context = {"event_index_active": "active", "platforms": platforms}
        return render(request, template, context)

    elif request.method == "POST":
        event_type_description = request.POST.get("event_type_description")
        event_recurrent = bool(request.POST.get("event_recurrent"))
        title = request.POST.get("title")
        description = request.POST.get("description")
        platform_name = request.POST.get("platform_name")
        other_platform = request.POST.get("other_platform")
        date_start = request.POST.get("date_start")
        date_end = request.POST.get("date_end")
        time_day = request.POST.get("time_day")
        record_date = request.POST.get("record_date")
        schedule_description = request.POST.get("schedule_description")

        # Event Type
        if event_type_description == "pre_recorded":
            is_recorded = True
        elif event_type_description in ["live_course", "event_single"]:
            is_recorded = False
        else:
            is_recorded = False

        if event_type_description in ["pre_recorded", "live_course"]:
            event_type = "COURSE"
        elif event_type_description in ["event_single", "event_recurrent"]:
            event_type = "EVENT"
        else:
            event_type = "COURSE"  # loggear exceptions

        # Connection Platform
        try:
            platform_obj = ConnectionPlatform.objects.get(name=platform_name)
        except Exception as e:
            platform_obj = None
            print(e)

        # Date & Time
        if len(date_start) > 0:
            date_start = datetime.strptime(date_start, "%d/%m/%Y")
        else:
            date_start = None
        if len(date_end) > 0:
            date_end = datetime.strptime(date_end, "%d/%m/%Y")
        else:
            date_end = None
        if len(time_day) > 0 and date_start is not None:
            time_day = datetime.strptime(time_day, "%I:%M %p")
            date_start.replace(hour=time_day.hour, minute=time_day.minute)

        if len(record_date) > 0:
            record_date = datetime.strptime(record_date, "%d/%m/%Y")
        else:
            record_date = None

        created_event = Event.objects.create(
            event_type=event_type,
            is_recorded=is_recorded,
            is_recurrent=event_recurrent,
            owner=request.user,
            title=title,
            description=description,
            platform=platform_obj,
            other_platform=other_platform,
            date_start=date_start,
            date_end=date_end,
            date_recorded=record_date,
            schedule_description=schedule_description
        )

        # Guardar imagen
        if "event_picture" in request.FILES:
            event_picture = request.FILES['event_picture']
            print("event_picture: %s" % event_picture.name)
            created_event.image.save(event_picture.name, event_picture)

        return redirect("event_detail", event_id=created_event.id)


# TODO bleach.clean para proteger inputs maliciosos
@login_required
def edit_event(request, event_id):
    if request.method == "GET":
        template = "courses/event_edit.html"
        event = get_object_or_404(Event, id=event_id)
        platforms = ConnectionPlatform.objects.filter(deleted=False)
        user_contact_methods = ContactMethod.objects.filter(user=event.owner)

        context = {"event": event, "platforms": platforms, "user_contact_methods": user_contact_methods}
        return render(request, template, context)

    elif request.method == "POST":
        event = get_object_or_404(Event, id=event_id)

        event_type_description = request.POST.get("event_type_description")
        event_recurrent = bool(request.POST.get("event_recurrent"))
        title = request.POST.get("title")
        description = request.POST.get("description")
        platform_name = request.POST.get("platform_name")
        other_platform = request.POST.get("other_platform")
        date_start = request.POST.get("date_start")
        date_end = request.POST.get("date_end")
        time_day = request.POST.get("time_day")
        record_date = request.POST.get("record_date")
        schedule_description = request.POST.get("schedule_description")

        print("time_day: %s" % time_day)

        # Event Type
        if event_type_description == "pre_recorded":
            is_recorded = True
        elif event_type_description in ["live_course", "event_single"]:
            is_recorded = False
        else:
            is_recorded = False

        if event_type_description in ["pre_recorded", "live_course"]:
            event_type = "COURSE"
        elif event_type_description in ["event_single", "event_recurrent"]:
            event_type = "EVENT"
        else:
            event_type = "COURSE"  # loggear exceptions

        # Connection Platform
        try:
            platform_obj = ConnectionPlatform.objects.get(name=platform_name)
        except Exception as e:
            platform_obj = None
            print(e)

        # Date & Time
        if len(date_start) > 0:
            date_start = datetime.strptime(date_start, "%d/%m/%Y")
        else:
            date_start = None
        if len(date_end) > 0:
            date_end = datetime.strptime(date_end, "%d/%m/%Y")
        else:
            date_end = None
        if len(time_day) > 0:
            time_day = datetime.strptime(time_day, "%I:%M %p")
            print("time_day.hour: %s" % time_day.hour)
            date_start = date_start.replace(hour=time_day.hour, minute=time_day.minute)
            print("date_start.hour: %s" % date_start.hour)
        if len(record_date) > 0:
            record_date = datetime.strptime(record_date, "%d/%m/%Y")
        else:
            record_date = None

        event.event_type = event_type
        event.is_recorded = is_recorded
        event.is_recurrent = event_recurrent
        event.owner = request.user
        event.title = title
        event.description = description
        event.platform = platform_obj
        event.other_platform = other_platform
        event.date_start = date_start
        event.date_end = date_end
        event.date_recorded = record_date
        event.schedule_description = schedule_description
        event.save()

        print("event.date_start.hour:%s" % event.date_start.hour)
        print("event.date_start.tzinfo:%s" % event.date_start.tzinfo)
        print("is_aware(event.date_start:%s)" % is_aware(event.date_start))

        # Guardar imagen
        if "event_picture" in request.FILES:
            event_picture = request.FILES['event_picture']
            print("event_picture: %s" % event_picture.name)
            event.image.save(event_picture.name, event_picture)

        return redirect("event_detail", event_id=event.id)


"""
API CALLS
"""


# TODO manejar cookie en el front, remover csrf_exempt

@login_required
@csrf_exempt
def event_bookmark(request, event_id):
    if request.is_ajax() and request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        if Bookmark.objects.filter(event=event, user=request.user, deleted=False).exists():
            print("bookmark ya existe")
            return HttpResponse(status=200)
        else:
            if Bookmark.objects.filter(event=event, user=request.user, deleted=True).exists():
                bookmark = Bookmark.objects.get(event=event, user=request.user, deleted=True)
                bookmark.deleted = False
                bookmark.save()
            else:
                Bookmark.objects.create(event=event, user=request.user)
            return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


@login_required
@csrf_exempt
def remove_bookmark(request, event_id):
    if request.is_ajax() and request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        if Bookmark.objects.filter(event=event, user=request.user, deleted=False).exists():
            bookmark = Bookmark.objects.get(user=request.user, event=event, deleted=False)
            bookmark.deleted = True
            bookmark.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

    else:
        return HttpResponse(status=403)


@login_required
@csrf_exempt
def request_certificate(request, event_id):
    if request.is_ajax() and request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        if CertificateRequest.objects.filter(event=event, user=request.user, deleted=False).exists():
            return HttpResponse(status=200)
        else:
            if CertificateRequest.objects.filter(event=event, user=request.user, deleted=True).exists():
                certificate_request = CertificateRequest.objects.get(event=event, user=request.user, deleted=True)
                certificate_request.deleted = False
                certificate_request.save()
            else:
                CertificateRequest.objects.create(event=event, user=request.user)
            return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


@login_required
@csrf_exempt
def cancel_cert_request(request, event_id):
    if request.is_ajax() and request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        if CertificateRequest.objects.filter(event=event, user=request.user, deleted=False).exists():
            certificate_request = CertificateRequest.objects.get(event=event, user=request.user, deleted=False)
            certificate_request.deleted = True
            certificate_request.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=400)


@login_required
@csrf_exempt
def accept_certificate(request, cert_request_id):
    if request.is_ajax() and request.method == "POST":
        certificate_request = get_object_or_404(CertificateRequest, id=cert_request_id)
        if request.user == certificate_request.event.owner:
            if Certificate.objects.filter(event=certificate_request.event, user=certificate_request.user).exists():
                pass
            else:
                Certificate.objects.create(event=certificate_request.event, user=certificate_request.user)
            certificate_request.accepted = True
            certificate_request.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)


def reject_certificate(request, cert_request_id):
    if request.is_ajax() and request.method == "POST":
        certificate_request = get_object_or_404(CertificateRequest, id=cert_request_id)
        if request.user == certificate_request.event.owner:
            if Certificate.objects.filter(event=certificate_request.event, user=certificate_request.user).exists():
                pass  # No puede rechazar si ya existe el certificado
            else:
                certificate_request.accepted = False
                certificate_request.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)
