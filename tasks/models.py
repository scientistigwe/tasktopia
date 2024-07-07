from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class Category(models.Model):
    """
    Model to represent a task category.
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
        if self.category_type == self.CategoryType.OTHER and self.category_name:
            return f"Other: {self.category_name}"
        return self.get_category_type_display()

class Task(models.Model):
    """
    Model to represent a task.
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
    is_manually_completed = models.BooleanField(default=False)  # Indicates if task is manually marked as completed

    def clean(self):
        """
        Ensure start_date is not later than due_date.
        """
        if self.start_date and self.due_date and self.start_date > self.due_date:
            raise ValidationError(_('Start date cannot be later than due date.'))

    def save(self, *args, **kwargs):
        """
        Clean the model instance and update its status before saving.
        """
        self.full_clean()
        self.update_status(save=False)
        super().save(*args, **kwargs)

    def update_status(self, save=False):
        """
        Automatically updates the task status based on current time and task dates.
        """
        now = timezone.now()

        if self.is_manually_completed or self.status == self.Status.COMPLETED:
            return
        # After Due Date (now > due_date):
        if now > self.due_date and self.status != self.Status.COMPLETED:
            self.status = self.Status.OVERDUE
        # During the Task Period (start_date <= now <= due_date):
        elif self.start_date <= now <= self.due_date:
            self.status = self.Status.IN_PROGRESS
        # Before Start Date (now < start_date)
        elif now < self.start_date:
            self.status = self.Status.PENDING

        if save:
            self.save(update_fields=['status'])

    def __str__(self):
        return f"Title: {self.title}, Priority: {self.priority}, Status: {self.status}"

class TaskRelationship(models.Model):
    """
    Model to represent the relationship between a task and a user.
    """
    task = models.OneToOneField(Task, on_delete=models.CASCADE, verbose_name=_('Task'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_relationships', verbose_name=_('User'))

    def __str__(self):
        return f"{self.user.username}: {self.task.title}"
