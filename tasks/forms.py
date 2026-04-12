# tasks/forms.py
# Contains the form for posting a new task.
# Used Django's ModelForm which automatically createsform fields based on our Task model.

from django import forms
from .models import Task, Skill, Category


class TaskForm(forms.ModelForm):
    # We override skills_required to use checkboxes instead of the default multi-select box
    skills_required = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # skills are optional
    )

    class Meta:
        model  = Task
        # we exclude client and status because:
        # client is set automatically to the logged-in user
        # status always starts as 'open' for new tasks
        fields = [
            'title',
            'description',
            'category',
            'skills_required',
            'budget_min',
            'budget_max',
            'deadline',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'e.g. Build a portfolio website'
            }),
            'description': forms.Textarea(attrs={
                'class':       'form-control',
                'rows':        5,
                'placeholder': 'Describe your task in detail...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'budget_min': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'Min budget ($)'
            }),
            'budget_max': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'Max budget ($)'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type':  'date'  # renders a date picker in the browser
            }),
        }

    def clean(self):
        # custom validation to make sure budget_min is not greater than budget_max
        cleaned_data = super().clean()
        budget_min   = cleaned_data.get('budget_min')
        budget_max   = cleaned_data.get('budget_max')

        if budget_min and budget_max:
            if budget_min > budget_max:
                raise forms.ValidationError(
                    "Minimum budget cannot be greater than maximum budget."
                )
        return cleaned_data
    