from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    priority = forms.ChoiceField(choices=Task.Priority.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=Task.Status.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M']  # Set input format for datetime-local field

    def save(self, user=None, commit=True):
        try:
            task = super().save(commit=False)
            if user:
                task.user = user  # Assign the current user to the task
            if commit:
                task.save()
            return task
        except Exception as e:
            print("Error during save:", e)
            raise e
