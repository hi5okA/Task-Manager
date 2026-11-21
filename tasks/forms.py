from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    ModelForm for Task creation and updating.
    Includes custom widgets with Bootstrap 5 styling and date input picker.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What needs to be done?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add optional description or details...'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
