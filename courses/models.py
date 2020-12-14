from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from profiles.models import AcceptedCrypto, Profile


def upload_event_picture(instance, filename):
    return "event_pictures/"+instance.title+"_"+datetime.today().strftime('%h-%d-%y')+".jpeg"


class Event(models.Model):
    """
    Puede ser un Curso grabado o en vivo, Conferencia, Actividad Recurrente y otros.
    """
    EVENT_TYPES = (("COURSE", "Course"),
                   ("EVENT", "Event"))
    is_recurrent = models.BooleanField(default=False, null=True)
    is_recorded = models.BooleanField(default=False, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, blank=True)
    image = models.ImageField(upload_to=upload_event_picture, null=True, blank=True)

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

    def __str__(self):
        return self.title


class ConnectionPlatform(models.Model):
    name = models.CharField(max_length=150, blank=True)
    url_link = models.URLField(blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title + " - " + self.user.username


class Bookmark(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.event.title + " - " + self.user.username


class CertificateRequest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    accepted = models.BooleanField(default=None, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.user.username + " - " + self.event.title
