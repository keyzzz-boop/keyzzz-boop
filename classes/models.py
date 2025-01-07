from django.db import models
from users.models import CustomUser
from courses.models import Course

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=20, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='teaching_classes', limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(CustomUser, blank=True,
        related_name='enrolled_classes', limit_choices_to={'role': 'student'})
    schedule = models.CharField(max_length=200, blank=True)
    room_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.code}"

    class Meta:
        ordering = ['name']
