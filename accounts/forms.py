from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2']


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'bio', 'profile_picture']


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'company_name', 'website', 'location', 'profile_picture']