from django.contrib import admin

from courses.models import Event, ConnectionPlatform, Bookmark, CertificateRequest, Certificate, Comment

admin.site.register(Event)
admin.site.register(ConnectionPlatform)
admin.site.register(Bookmark)
admin.site.register(CertificateRequest)
admin.site.register(Certificate)
admin.site.register(Comment)
