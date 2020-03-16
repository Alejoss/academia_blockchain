from django.contrib import admin


from exams.models import Exam, ExamTaken

admin.site.register(Exam)
admin.site.register(ExamTaken)
