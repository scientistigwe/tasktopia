from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    priority = forms.ChoiceField(choices=Task.Priority.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=Task.Status.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'due_date', 'priority', 'status', 'category']

    def __init__(self, *args, **kwargs):
        """
        Set input format for datetime-local field
        """
        super().__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ['%Y-%m-%dT%H:%M'] 
        self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M'] 

    def save(self, user=None, commit=True):
        """
        Assign the current user to the task
        """
        try:
            task = super().save(commit=False)
            if user:
                task.user = user
            if commit:
                task.save()
            return task
        except Exception as e:
            print("Error during save:", e)
            raise e
