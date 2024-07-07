from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task instances.
    """
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        error_messages={'required': 'Please enter a title.'}
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}),
        error_messages={'required': 'Please enter a description.'}
    )
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'required': 'required'}),
        error_messages={'required': 'Please enter a start date.'}
    )
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'required': 'required'}),
        error_messages={'required': 'Please enter a due date.'}
    )
    priority = forms.ChoiceField(
        choices=Task.Priority.choices,
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        error_messages={'required': 'Please select a priority.'}
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'due_date', 'priority']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if start_date and due_date and start_date > due_date:
            self.add_error('due_date', "Due date cannot be earlier than start date.")
        
        return cleaned_data

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
    
class CategoryForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('church', 'Church'),
        ('work', 'Work'),
        ('walkout', 'Walkout'),
        ('other', 'Other (Specify)'),
    ]

    category_type = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={'required': 'Please select a category type.'}
    )
    category_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Please enter a category name.'}
    )

    class Meta:
        model = Category
        fields = ['category_type', 'category_name']

    def clean(self):
        cleaned_data = super().clean()
        category_type = cleaned_data.get('category_type')
        category_name = cleaned_data.get('category_name')

        if category_type == 'other' and not category_name:
            self.add_error('category_name', 'Please specify the category name.')

        return cleaned_data

class MarkTaskAsCompletedForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
