from django.contrib import admin

from profiles.models import Profile, AcceptedCrypto, ContactMethod

admin.site.register(Profile)
admin.site.register(AcceptedCrypto)
admin.site.register(ContactMethod)
