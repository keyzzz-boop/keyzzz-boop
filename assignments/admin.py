from django.contrib import admin
from .models import Assignment, AssignmentSubmission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'classroom', 'uploaded_by', 'due_date', 'max_marks']

@admin.register(AssignmentSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'is_graded', 'marks']
