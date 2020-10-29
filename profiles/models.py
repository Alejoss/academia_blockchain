from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interests = models.CharField(max_length=250, blank=True)
    profile_description = models.TextField(max_length=2500, blank=True)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def cryptos_list(self):
        return [crypto for crypto in AcceptedCrypto.objects.filter(user=self.user)]


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True)
    code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class AcceptedCrypto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    crypto = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=250, blank=True)
    deleted = models.BooleanField(default=False)


class ContactMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=250, blank=True)
    url_link = models.CharField(max_length=250, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
