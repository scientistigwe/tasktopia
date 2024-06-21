from django import forms
from .models import TaskRelationship, Task, Category

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    priority = forms.ChoiceField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = TaskRelationship
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'category']

    def save(self, commit=True):
        task_relationship = super().save(commit=False)
        task_data = {
            'title': self.cleaned_data['title'],
            'description': self.cleaned_data['description'],
            'due_date': self.cleaned_data['due_date'],
            'priority': self.cleaned_data['priority'],
            'status': self.cleaned_data['status'],
            'category': self.cleaned_data['category']
        }
        task = Task.objects.create(**task_data)
        task_relationship.task = task
        if commit:
            task_relationship.save()
        return task_relationship

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']
