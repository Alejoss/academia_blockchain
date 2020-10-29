from django.contrib import admin

from profiles.models import Profile, AcceptedCrypto, ContactMethod, CryptoCurrency

admin.site.register(Profile)
admin.site.register(AcceptedCrypto)
admin.site.register(ContactMethod)
admin.site.register(CryptoCurrency)
