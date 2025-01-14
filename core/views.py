from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from courses.models import Course
from classes.models import Classroom
from attendance.models import AttendanceSession, AttendanceRecord
from assignments.models import Assignment, AssignmentSubmission



@login_required
def dashboard(request):
    u = request.user
    ctx = {}
    if u.is_admin:
        ctx['total_students'] = CustomUser.objects.filter(role='student').count()
        ctx['total_teachers'] = CustomUser.objects.filter(role='teacher').count()
        ctx['total_courses'] = Course.objects.count()
        ctx['total_classes'] = Classroom.objects.count()
        ctx['recent_sessions'] = AttendanceSession.objects.select_related('classroom','taken_by').order_by('-date')[:5]
        ctx['recent_assignments'] = Assignment.objects.select_related('classroom','uploaded_by').order_by('-created_at')[:5]
    elif u.is_teacher:
        my_classes = Classroom.objects.filter(teacher=u)
        ctx['my_classes'] = my_classes
        ctx['total_students'] = sum(c.students.count() for c in my_classes)
        ctx['my_courses'] = Course.objects.filter(teacher=u).count()
        ctx['recent_assignments'] = Assignment.objects.filter(uploaded_by=u).order_by('-created_at')[:5]
        ctx['recent_sessions'] = AttendanceSession.objects.filter(taken_by=u).order_by('-date')[:5]
    else:
        ctx['my_courses'] = u.enrolled_courses.all()
        ctx['my_classes'] = u.enrolled_classes.select_related('teacher', 'course').all()
        
        ctx['recent_assignments'] = Assignment.objects.filter(classroom__in=u.enrolled_classes.all()).order_by('-created_at')[:5]
        ctx['attendance_pct'] = _student_attendance_pct(u)
    return render(request, 'core/dashboard.html', ctx)


def _student_attendance_pct(student):
    total = AttendanceRecord.objects.filter(student=student).count()
    present = AttendanceRecord.objects.filter(student=student, status__in=['present','late']).count()
    return round(present / total * 100, 1) if total > 0 else 0
