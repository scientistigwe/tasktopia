"""
Forms for creating and updating Task and Category instances.
"""

from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task instances.

    Attributes:
        title (CharField): The title of the task.
        description (CharField): The description of the task.
        start_date (DateTimeField): The start date and time of the task.
        due_date (DateTimeField): The due date and time of the task.
        priority (ChoiceField): The priority level of the task.
    
    Methods:
        clean(): Validates the form instance to ensure start_date is not later than due_date.
        save(commit=True): Saves the form and assigns the current user to the task.
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
        """
        Validates the form instance to ensure start_date is not later than due_date.

        Raises:
            ValidationError: If start_date is later than due_date.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if start_date and due_date and start_date > due_date:
            self.add_error('due_date', "Due date cannot be earlier than start date.")
        
        return cleaned_data

    def save(self, commit=True):
        """
        Saves the form and assigns the current user to the task.

        Args:
            commit (bool, optional): If True, saves the task instance to the database. Defaults to True.

        Returns:
            Task: The saved task instance.
        """
        task = super().save(commit=False)
        if self.instance.user:
            task.user = self.instance.user
        if commit:
            task.save()
        return task


class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating Category instances.

    Attributes:
        category_type (ChoiceField): The type of the category.
        category_name (CharField): The name of the category.

    Methods:
        clean(): Validates the form instance to ensure category_name is provided if category_type is 'other'.
    """

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
        """
        Validates the form instance to ensure category_name is provided if category_type is 'other'.

        Raises:
            ValidationError: If category_type is 'other' and category_name is not provided.
        """
        cleaned_data = super().clean()
        category_type = cleaned_data.get('category_type')
        category_name = cleaned_data.get('category_name')

        if category_type == 'other' and not category_name:
            self.add_error('category_name', 'Please specify the category name.')

        return cleaned_data
