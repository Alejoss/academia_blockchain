from datetime import datetime
import logging

from courses.models import ConnectionPlatform

logger = logging.getLogger('app_logger')


def get_event_data_request(request):
    """
    :param request: request django object with form data
    :return: dict with processed data after logging
    """
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
    tags = request.POST.getlist("tags[]")

    logger.info("event_type_description: %s" % event_type_description)
    logger.info("event_recurrent: %s" % event_recurrent)
    logger.info("title: %s" % title)
    logger.info("description: %s" % description)
    logger.info("platform_name: %s" % platform_name)
    logger.info("other_platform: %s" % other_platform)
    logger.info("date_start: %s" % date_start)
    logger.info("date_end: %s" % date_end)
    logger.info("time_day: %s" % time_day)
    logger.info("record_date: %s" % record_date)
    logger.info("schedule_description: %s" % schedule_description)

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

    # Connection Platform
    try:
        platform_obj = ConnectionPlatform.objects.get(name=platform_name)
    except Exception as e:
        logger.warning("ERROR saving platform name")
        logger.warning(e)
        platform_obj = None

    event_data = {
            "event_type": event_type,
            "is_recorded": is_recorded,
            "event_recurrent": event_recurrent,
            "title": title,
            "description": description,
            "platform": platform_obj,
            "other_platform": other_platform,
            "date_start": date_start,
            "date_end": date_end,
            "time_day": time_day,
            "record_date": record_date,
            "schedule_description": schedule_description,
            "tags": tags
        }

    return event_data
