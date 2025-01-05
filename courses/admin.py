from django.contrib import admin
from .models import Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'teacher', 'credits']
    filter_horizontal = ['students']
