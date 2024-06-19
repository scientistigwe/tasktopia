# tasks/forms.py

from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'category', 'user']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'priority': forms.Select(),
            'status': forms.Select(),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']
