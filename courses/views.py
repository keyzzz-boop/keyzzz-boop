from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from users.models import CustomUser


@login_required
def course_list(request):
    u = request.user
    if u.is_admin:
        courses = Course.objects.select_related('teacher').prefetch_related('students')
    elif u.is_teacher:
        courses = Course.objects.filter(teacher=u)
    else:
        courses = u.enrolled_courses.select_related('teacher')
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})


@login_required
def create_course(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('course_list')
    teachers = CustomUser.objects.filter(role='teacher')
    students = CustomUser.objects.filter(role='student')
    if request.method == 'POST':
        p = request.POST
        if Course.objects.filter(code=p['code']).exists():
            messages.error(request, 'Course code already exists.')
        else:
            c = Course(name=p['name'], code=p['code'],
                       description=p.get('description',''), credits=p.get('credits',3))
            tid = p.get('teacher')
            if tid: c.teacher_id = tid
            c.save()
            c.students.set(p.getlist('students'))
            messages.success(request, 'Course created!')
            return redirect('course_list')
    return render(request, 'courses/course_form.html', {
        'title':'Create Course','action':'Create','teachers':teachers,'students':students})


@login_required
def edit_course(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('course_list')
    course = get_object_or_404(Course, pk=pk)
    teachers = CustomUser.objects.filter(role='teacher')
    students = CustomUser.objects.filter(role='student')
    if request.method == 'POST':
        p = request.POST
        course.name = p['name']
        course.code = p['code']
        course.description = p.get('description','')
        course.credits = p.get('credits',3)
        tid = p.get('teacher')
        course.teacher_id = tid if tid else None
        course.save()
        course.students.set(p.getlist('students'))
        messages.success(request, 'Course updated!')
        return redirect('course_list')
    return render(request, 'courses/course_form.html', {
        'title':'Edit Course','action':'Update','course':course,
        'teachers':teachers,'students':students})


@login_required
def delete_course(request, pk):
    if not request.user.is_admin:
        return redirect('course_list')
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('course_list')
    return render(request, 'courses/confirm_delete.html', {'obj': course, 'cancel_url': 'course_list'})
