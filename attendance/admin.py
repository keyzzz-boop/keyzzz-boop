from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord

class RecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0

@admin.register(AttendanceSession)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'date', 'taken_by']
    inlines = [RecordInline]
