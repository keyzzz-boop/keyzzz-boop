from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_list(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    role = request.GET.get('role', '')
    users = CustomUser.objects.exclude(pk=request.user.pk)
    if role:
        users = users.filter(role=role)
    return render(request, 'users/user_list.html', {'users': users, 'role_filter': role})


@login_required
def create_user(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    if request.method == 'POST':
        p = request.POST
        if p.get('password') != p.get('confirm_password'):
            messages.error(request, 'Passwords do not match.')
        elif CustomUser.objects.filter(username=p['username']).exists():
            messages.error(request, 'Username already exists.')
        else:
            u = CustomUser(
                username=p['username'], first_name=p.get('first_name',''),
                last_name=p.get('last_name',''), email=p.get('email',''),
                role=p['role'], phone=p.get('phone',''), address=p.get('address',''),
            )
            if p.get('date_of_birth'):
                u.date_of_birth = p['date_of_birth']
            u.set_password(p['password'])
            u.save()
            messages.success(request, f"User '{u.username}' created!")
            return redirect('user_list')
    return render(request, 'users/user_form.html', {'title': 'Create User', 'action': 'Create'})


@login_required
def edit_user(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    u = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        p = request.POST
        u.first_name = p.get('first_name', '')
        u.last_name = p.get('last_name', '')
        u.email = p.get('email', '')
        u.role = p.get('role', u.role)
        u.phone = p.get('phone', '')
        u.address = p.get('address', '')
        if p.get('date_of_birth'):
            u.date_of_birth = p['date_of_birth']
        if p.get('password'):
            u.set_password(p['password'])
        u.save()
        messages.success(request, 'User updated!')
        return redirect('user_list')
    return render(request, 'users/user_form.html', {'title': 'Edit User', 'action': 'Update', 'user_obj': u})


@login_required
def delete_user(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    u = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        u.delete()
        messages.success(request, 'User deleted.')
        return redirect('user_list')
    return render(request, 'users/confirm_delete.html', {'obj': u, 'cancel_url': 'user_list'})


@login_required
def profile(request):
    u = request.user
    if request.method == 'POST':
        p = request.POST
        u.first_name = p.get('first_name', '')
        u.last_name = p.get('last_name', '')
        u.email = p.get('email', '')
        u.phone = p.get('phone', '')
        u.address = p.get('address', '')
        if p.get('date_of_birth'):
            u.date_of_birth = p['date_of_birth']
        if p.get('password'):
            u.set_password(p['password'])
            u.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, u)
        else:
            u.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile')
    return render(request, 'users/profile.html', {'user_obj': u})
