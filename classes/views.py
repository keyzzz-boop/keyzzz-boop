from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Classroom
from courses.models import Course
from users.models import CustomUser


@login_required
def class_list(request):
    u = request.user
    if u.is_admin:
        classes = Classroom.objects.select_related('course', 'teacher')
    elif u.is_teacher:
        classes = Classroom.objects.filter(teacher=u).select_related('course')
    else:
        classes = u.enrolled_classes.select_related('course', 'teacher')
    return render(request, 'classes/class_list.html', {'classes': classes})


@login_required
def class_detail(request, pk):
    cls = get_object_or_404(Classroom, pk=pk)
    return render(request, 'classes/class_detail.html', {'cls': cls})


@login_required
def create_class(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('class_list')
    courses = Course.objects.all()
    teachers = CustomUser.objects.filter(role='teacher')
    students = CustomUser.objects.filter(role='student')
    if request.method == 'POST':
        p = request.POST
        cls = Classroom(
            name=p['name'], section=p.get('section',''),
            course_id=p['course'], schedule=p.get('schedule',''),
            room_number=p.get('room_number','')
        )
        tid = p.get('teacher')
        if tid: cls.teacher_id = tid
        cls.save()
        cls.students.set(p.getlist('students'))
        messages.success(request, 'Class created!')
        return redirect('class_list')
    return render(request, 'classes/class_form.html', {
        'title':'Create Class','action':'Create',
        'courses':courses,'teachers':teachers,'students':students})


@login_required
def edit_class(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('class_list')
    cls = get_object_or_404(Classroom, pk=pk)
    courses = Course.objects.all()
    teachers = CustomUser.objects.filter(role='teacher')
    students = CustomUser.objects.filter(role='student')
    if request.method == 'POST':
        p = request.POST
        cls.name = p['name']
        cls.section = p.get('section','')
        cls.course_id = p['course']
        cls.schedule = p.get('schedule','')
        cls.room_number = p.get('room_number','')
        tid = p.get('teacher')
        cls.teacher_id = tid if tid else None
        cls.save()
        cls.students.set(p.getlist('students'))
        messages.success(request, 'Class updated!')
        return redirect('class_list')
    return render(request, 'classes/class_form.html', {
        'title':'Edit Class','action':'Update','cls':cls,
        'courses':courses,'teachers':teachers,'students':students})


@login_required
def delete_class(request, pk):
    if not request.user.is_admin:
        return redirect('class_list')
    cls = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        cls.delete()
        messages.success(request, 'Class deleted.')
        return redirect('class_list')
    return render(request, 'classes/confirm_delete.html', {'obj': cls, 'cancel_url': 'class_list'})
