from django import forms
from .models import Task, Category
from django.core.exceptions import ValidationError

class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task instances.
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    priority = forms.ChoiceField(choices=Task.Priority.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'due_date', 'priority', 'category']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set input formats for datetime fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ['%Y-%m-%dT%H:%M'] 
        self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M']

    def save(self, user=None, commit=True):
        """
        Save the form and assign the current user to the task.
        """
        task = super().save(commit=False)
        if user:
            task.user = user
        if commit:
            task.save()
        return task
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if start_date and due_date and start_date > due_date:
            raise ValidationError("Start date cannot be later than due date.")

        return cleaned_data

class MarkTaskAsCompletedForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']