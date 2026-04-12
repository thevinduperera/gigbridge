from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('login')  # or home
    return render(request, 'accounts/client_dashboard.html')


@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return redirect('login')  # or home
    return render(request, 'accounts/freelancer_dashboard.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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
                return redirect('client_dashboard')
            elif user.role == 'freelancer':
                return redirect('freelancer_dashboard')

            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})