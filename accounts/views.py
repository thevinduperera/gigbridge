# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from core.models import Notification

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('accounts:login')
    return render(request, 'tasks/client_dashboard.html')


@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return redirect('accounts:login')
    return render(request, 'tasks/freelancer_dashboard.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # redirect to correct dashboard based on role
            if user.role == 'client':
                return redirect('tasks:client_dashboard')
            elif user.role == 'freelancer':
                return redirect('tasks:freelancer_dashboard')
            return redirect('core:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})