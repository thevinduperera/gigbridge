from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, FreelancerProfileForm
from .models import User


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


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

            if user.role == 'client':
                return redirect('tasks:client_dashboard')
            elif user.role == 'freelancer':
                return redirect('tasks:freelancer_dashboard')
            return redirect('core:home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def freelancer_profile_edit_view(request):
    if request.user.role != 'freelancer':
        return redirect('core:home')

    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:freelancer_profile_view')
    else:
        form = FreelancerProfileForm(instance=request.user)

    return render(request, 'accounts/freelancer_profile_edit.html', {'form': form})


@login_required
def freelancer_profile_view(request):
    if request.user.role != 'freelancer':
        return redirect('core:home')

    return render(request, 'accounts/freelancer_profile_view.html', {
        'user_profile': request.user
    })


def public_freelancer_profile_view(request, username):
    user_profile = get_object_or_404(User, username=username, role='freelancer')

    return render(request, 'accounts/public_freelancer_profile.html', {
        'user_profile': user_profile
    })