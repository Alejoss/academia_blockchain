from http import HTTPStatus
import pytz
import json
from http import HTTPStatus
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user
from django.http import HttpResponse

from courses.models import Event, ConnectionPlatform
from profiles.models import ContactMethod, AcceptedCrypto

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
    print("event.date_start.hour:%s" % event.date_start.hour)

    contact_methods = ContactMethod.objects.filter(user=event.owner, deleted=False)
    accepted_cryptos = AcceptedCrypto.objects.filter(user=event.owner, deleted=False)

    context = {"event": event, "contact_methods": contact_methods, "accepted_cryptos": accepted_cryptos}
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
        time_zone = request.POST.get("time_zone")
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
        time_zone_obj = pytz.timezone("Etc/" + time_zone)  # pytz format
        if len(date_start) > 0:
            date_start = datetime.strptime(date_start, "%d/%m/%Y")
            date_start = date_start.replace(tzinfo=time_zone_obj)
        else:
            date_start = None
        if len(date_end) > 0:
            date_end = datetime.strptime(date_end, "%d/%m/%Y")
            date_end = date_end.replace(tzinfo=time_zone_obj)
        else:
            date_end = None
        if len(time_day) > 0:
            time_day = datetime.strptime(time_day, "%I:%M %p")
            date_start.replace(hour=time_day.hour, minute=time_day.minute)
        else:
            time_day = None
        if len(record_date) > 0:
            record_date = datetime.strptime(record_date, "%d/%m/%Y")
            record_date = record_date.replace(tzinfo=time_zone_obj)
        else:
            record_date = None

        print("date_start: %s" % date_start)
        print("date_end: %s" % date_end)
        print("time_day: %s" % time_day)
        print("time_zone: %s" % time_zone)
        print("record_date: %s" % record_date)

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
        # event_picture = request.FILES['event_picture']
        # print("event_picture: %s" % event_picture)
        # created_event.image = event_picture
        # created_event.image.save()

        print("event_type_description: %s" % event_type_description)
        print("title: %s" % title)
        print("description: %s" % description)
        print("platform_name: %s" % platform_name)
        print("other_platform: %s" % other_platform)

        return redirect("event_detail", event_id=created_event.id)


@login_required
def edit_event(request, event_id):
    if request.method == "GET":
        template = "courses/event_edit.html"
        event = get_object_or_404(Event, id=event_id)
        platforms = ConnectionPlatform.objects.filter(deleted=False)

        context = {"event": event, "platforms": platforms}
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
        time_zone = request.POST.get("time_zone")
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
        time_zone_obj = pytz.timezone("Etc/" + time_zone)  # pytz format
        if len(date_start) > 0:
            date_start = datetime.strptime(date_start, "%d/%m/%Y")
            date_start = date_start.replace(tzinfo=time_zone_obj)
        else:
            date_start = None
        if len(date_end) > 0:
            date_end = datetime.strptime(date_end, "%d/%m/%Y")
            date_end = date_end.replace(tzinfo=time_zone_obj)
        else:
            date_end = None
        if len(time_day) > 0:
            time_day = datetime.strptime(time_day, "%I:%M %p")
            print("time_day.hour: %s" % time_day.hour)
            date_start = date_start.replace(hour=time_day.hour, minute=time_day.minute)
            print("date_start.hour: %s" % date_start.hour)
        if len(record_date) > 0:
            record_date = datetime.strptime(record_date, "%d/%m/%Y")
            record_date = record_date.replace(tzinfo=time_zone_obj)
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

        # Guardar imagen
        # event_picture = request.FILES['event_picture']
        # print("event_picture: %s" % event_picture)
        # created_event.image = event_picture
        # created_event.image.save()

        return redirect("event_detail", event_id=event.id)


"""
API CALLS
"""
