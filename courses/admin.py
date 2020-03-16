from django.contrib import admin


from courses.models import Course, AcceptedCrypto

admin.site.register(Course)
admin.site.register(AcceptedCrypto)
