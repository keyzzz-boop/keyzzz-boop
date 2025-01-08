from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AttendanceSession, AttendanceRecord
from classes.models import Classroom
from users.models import CustomUser


@login_required
def attendance_list(request):
    u = request.user
    if u.is_admin:
        sessions = AttendanceSession.objects.select_related('classroom', 'taken_by').order_by('-date')
    elif u.is_teacher:
        sessions = AttendanceSession.objects.filter(taken_by=u).select_related('classroom').order_by('-date')
    else:
        sessions = AttendanceSession.objects.filter(
            classroom__in=u.enrolled_classes.all()
        ).order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'sessions': sessions})


@login_required
def take_attendance(request, class_id):
    if not (request.user.is_teacher or request.user.is_admin):
        messages.error(request, 'Access denied.')
        return redirect('attendance_list')
    classroom = get_object_or_404(Classroom, pk=class_id)
    if request.user.is_teacher and classroom.teacher != request.user:
        messages.error(request, 'You are not assigned to this class.')
        return redirect('attendance_list')
    today = timezone.now().date()
    date_str = request.GET.get('date', str(today))
    try:
        from datetime import date
        selected_date = date.fromisoformat(date_str)
    except:
        selected_date = today

    session, created = AttendanceSession.objects.get_or_create(
        classroom=classroom, date=selected_date,
        defaults={'taken_by': request.user}
    )
    students = classroom.students.all()

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.pk}', 'absent')
            note = request.POST.get(f'note_{student.pk}', '')
            AttendanceRecord.objects.update_or_create(
                session=session, student=student,
                defaults={'status': status, 'note': note}
            )
        messages.success(request, 'Attendance saved!')
        return redirect('attendance_list')

    existing = {r.student_id: r for r in session.records.all()}
    student_data = []
    for s in students:
        rec = existing.get(s.pk)
        student_data.append({
            'student': s,
            'status': rec.status if rec else 'present',
            'note': rec.note if rec else '',
        })
    return render(request, 'attendance/take_attendance.html', {
        'classroom': classroom, 'date': selected_date,
        'student_data': student_data, 'session': session,
    })


@login_required
def attendance_report(request, class_id):
    classroom = get_object_or_404(Classroom, pk=class_id)
    sessions = AttendanceSession.objects.filter(classroom=classroom).prefetch_related('records__student').order_by('date')
    students = classroom.students.all()
    report = []
    for student in students:
        total = sessions.count()
        present = AttendanceRecord.objects.filter(session__classroom=classroom, student=student, status='present').count()
        late = AttendanceRecord.objects.filter(session__classroom=classroom, student=student, status='late').count()
        absent = total - present - late
        pct = round((present + late) / total * 100, 1) if total > 0 else 0
        report.append({'student': student, 'present': present, 'late': late, 'absent': absent, 'total': total, 'pct': pct})
    return render(request, 'attendance/attendance_report.html', {
        'classroom': classroom, 'report': report, 'sessions': sessions
    })


@login_required
def session_detail(request, session_id):
    session = get_object_or_404(AttendanceSession, pk=session_id)
    records = session.records.select_related('student').all()
    return render(request, 'attendance/session_detail.html', {'session': session, 'records': records})
