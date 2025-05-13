from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreateForm, UserUpdateForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages

def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'users/create_user.html', {'form': form})

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated.')
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/update_user.html', {'form': form, 'user_id': user_id})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted.')
    return redirect('user_list')

def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, 'Password changed.')
            return redirect('user_list')
    else:
        form = ChangePasswordForm()
    return render(request, 'users/change_password.html', {'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})
