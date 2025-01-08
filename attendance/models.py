from django.db import models
from users.models import CustomUser
from classes.models import Classroom


class AttendanceSession(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    taken_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['classroom', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.classroom} - {self.date}"


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [('present','Present'),('absent','Absent'),('late','Late')]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'})
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.student} - {self.status}"
