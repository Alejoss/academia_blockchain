from django.contrib import admin

from courses.models import Event, ConnectionPlatform, Bookmark

admin.site.register(Event)
admin.site.register(ConnectionPlatform)
admin.site.register(Bookmark)
