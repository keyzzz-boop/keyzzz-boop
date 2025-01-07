from django.contrib import admin
from .models import Classroom
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'course', 'teacher']
    filter_horizontal = ['students']
