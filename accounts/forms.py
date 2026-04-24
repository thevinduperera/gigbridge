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
        fields = [
            'username',
            'headline',
            'bio',
            'skills',
            'rate',
            'portfolio',
            'availability',
            'profile_picture',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'bio':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': f'Enter {field.label.lower()}'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f'Enter {field.label.lower()}'
                })


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'company_name', 'website', 'location', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field.label.lower()}'
            })