from django.db import models

from profiles.models import Profile


class Exam(models.Model):
    accreditor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=10000, blank=True)


class ExamTaken(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    grade = models.SmallIntegerField(null=True, blank=True)
    certificate_hash = models.CharField(max_length=150)  # Hash to be saved on a blockchain
