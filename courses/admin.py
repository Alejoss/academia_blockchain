from django.contrib import admin

from courses.models import Event, ConnectionPlatform, Bookmark, CertificateRequest, Certificate

admin.site.register(Event)
admin.site.register(ConnectionPlatform)
admin.site.register(Bookmark)
admin.site.register(CertificateRequest)
admin.site.register(Certificate)
