from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_description = models.CharField(max_length=1000)
    is_teacher = models.BooleanField(default=False)
    is_accreditor = models.BooleanField(default=False)


