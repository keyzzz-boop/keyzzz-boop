from django.db import models
from users.models import CustomUser

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=3)
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='teaching_courses', limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(CustomUser, blank=True,
        related_name='enrolled_courses', limit_choices_to={'role': 'student'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
