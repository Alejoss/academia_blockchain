from django.db import models
from django.contrib.auth.models import User

from profiles.models import AcceptedCrypto, Profile


class Event(models.Model):
    """
    Puede ser un Curso grabado o en vivo, Conferencia, Actividad Recurrente y otros.
    """
    EVENT_TYPES = (("COURSE", "Course"),
                   ("EVENT", "Event"))
    is_recurrent = models.BooleanField(default=False, null=True)
    is_recorded = models.BooleanField(default=False, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, blank=True)

    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=10000, blank=True)
    platform = models.ForeignKey('ConnectionPlatform', null=True, on_delete=models.CASCADE, blank=True)
    other_platform = models.CharField(max_length=150, blank=True)
    reference_price = models.FloatField(default=0, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    date_recorded = models.DateTimeField(null=True, blank=True)
    schedule_description = models.CharField(max_length=1000, blank=True)  # da flexibilidad

    # TODO instalar un sistema de tags. django-taggit probablemente

    def __str__(self):
        return self.title


class ConnectionPlatform(models.Model):
    name = models.CharField(max_length=150, blank=True)
    url_link = models.URLField(blank=True)
    deleted = models.BooleanField(default=False)
