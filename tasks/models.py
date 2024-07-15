"""
Models for tasks and categories.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """
    A model to represent a task category.

    Attributes:
        category_id (AutoField): The primary key for the category.
        category_name (CharField): The name of the category (optional).
        category_type (CharField): The type of the category, using choices defined in CategoryType.
        created_at (DateTimeField): The date and time when the category was created.
        user (ForeignKey): The user associated with this category.

    Methods:
        __str__(): Returns a string representation of the category, either displaying its type or 'Other' with a custom name.
    """

    class CategoryType(models.TextChoices):
        PERSONAL = 'personal', _('Personal')
        CHURCH = 'church', _('Church')
        WORK = 'work', _('Work')
        WALKOUT = 'walkout', _('Walkout')
        OTHER = 'other', _('Other')

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=225, blank=True, null=True)
    category_type = models.CharField(
        max_length=10,
        choices=CategoryType.choices,
        default=CategoryType.PERSONAL,
        verbose_name=_('Category Type')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_categories')

    def __str__(self):
        """
        Returns a string representation of the category.
        
        Returns:
            str: The category type or 'Other' with the custom name, if provided.
        """
        if self.category_type == self.CategoryType.OTHER and self.category_name:
            return f"Other: {self.category_name}"
        return self.get_category_type_display()

class Task(models.Model):
    """
    A model to represent a task.

    Attributes:
        task_id (AutoField): The primary key for the task.
        title (CharField): The title of the task.
        description (TextField): A detailed description of the task.
        start_date (DateTimeField): The start date and time of the task.
        due_date (DateTimeField): The due date and time of the task.
        priority (CharField): The priority level of the task, using choices defined in Priority.
        status (CharField): The current status of the task, using choices defined in Status.
        completion_date (DateTimeField, optional): The date and time when the task was completed (if applicable).
        created_at (DateTimeField): The date and time when the task was created.
        updated_at (DateTimeField): The date and time when the task was last updated.
        category (ForeignKey): The category associated with this task.
        user (ForeignKey): The user who owns this task.
        is_manually_completed (BooleanField): Indicates if the task was manually marked as completed.

    Methods:
        clean(): Validates the task instance to ensure start_date is not later than due_date.
        save(*args, **kwargs): Saves the task instance and updates its status.
        update_status(save=False): Automatically updates the task status based on current time and dates.
        __str__(): Returns a string representation of the task, displaying its title, priority, and status.
    """

    class Priority(models.TextChoices):
        HIGH = 'High', _('High')
        MEDIUM = 'Medium', _('Medium')
        LOW = 'Low', _('Low')

    class Status(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        COMPLETED = 'Completed', _('Completed')
        OVERDUE = 'Overdue', _('Overdue')
        IN_PROGRESS = 'In Progress', _('In Progress')

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    due_date = models.DateTimeField(verbose_name=_('Due Date'))
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM, verbose_name=_('Priority'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('Status'))
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Completion Date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('Category'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('User'))
    is_manually_completed = models.BooleanField(default=False)

    def clean(self):
        """
        Validates the task instance to ensure start_date is not later than due_date.
        
        Raises:
            ValidationError: If start_date is later than due_date.
        """
        if self.start_date and self.due_date and self.start_date > self.due_date:
            raise ValidationError(_('Start date cannot be later than due date.'))

    def save(self, *args, **kwargs):
        """
        Saves the task instance and updates its status.
        """
        self.full_clean()
        self.update_status(save=False)
        super().save(*args, **kwargs)

    def update_status(self, save=False):
        """
        Automatically updates the task status based on current time and dates.

        Args:
            save (bool, optional): If True, saves the updated status to the database. Defaults to False.
        """
        now = timezone.now()

        if self.is_manually_completed or self.status == self.Status.COMPLETED:
            return

        if now > self.due_date and self.status != self.Status.COMPLETED:
            self.status = self.Status.OVERDUE
        elif self.start_date <= now <= self.due_date:
            self.status = self.Status.IN_PROGRESS
        elif now < self.start_date:
            self.status = self.Status.PENDING

        if save:
            self.save(update_fields=['status'])

    def __str__(self):
        """
        Returns a string representation of the task.

        Returns:
            str: The title, priority, and status of the task.
        """
        return f"Title: {self.title}, Priority: {self.priority}, Status: {self.status}"

class TaskRelationship(models.Model):
    """
    A model to represent the relationship between a task and a user.

    Attributes:
        task (OneToOneField): The task associated with this relationship.
        user (ForeignKey): The user associated with this relationship.

    Methods:
        __str__(): Returns a string representation of the task relationship, displaying the user's username and the task's title.
    """

    task = models.OneToOneField(Task, on_delete=models.CASCADE, verbose_name=_('Task'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_relationships', verbose_name=_('User'))

    def __str__(self):
        """
        Returns a string representation of the task relationship.

        Returns:
            str: The username of the user and the title of the associated task.
        """
        return f"{self.user.username}: {self.task.title}"
