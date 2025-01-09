from django.db import models
from users.models import CustomUser
from classes.models import Classroom


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_assignments')
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    max_marks = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.classroom})"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    is_graded = models.BooleanField(default=False)

    class Meta:
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
