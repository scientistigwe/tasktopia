from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    """
    Represents a task with various attributes such as priority, status, and progress.
    """
    is_manually_completed = models.BooleanField(default=False)

    class Priority(models.TextChoices):
        HIGH = 'High', 'High'
        MEDIUM = 'Medium', 'Medium'
        LOW = 'Low', 'Low'

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        COMPLETED = 'Completed', 'Completed'
        OVERDUE = 'Overdue', 'Overdue'
        IN_PROGRESS = 'In Progress', 'In Progress'

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    completion_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_tasks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_tasks')

    def update_status(self, save=False):
        """
        Automatically updates the status based on progress, start date, and due date,
        but skips the update if the task is manually marked as completed or already completed.
        """
        now = timezone.now()

        # Skip automatic update if the task is manually marked as completed or already completed
        if self.is_manually_completed or self.status == self.Status.COMPLETED:
            return

        # Logic to determine the task's status
        if now > self.due_date and self.status != self.Status.COMPLETED:
            self.status = self.Status.OVERDUE
        elif self.start_date <= now <= self.due_date:
            self.status = self.Status.IN_PROGRESS
        elif now < self.start_date:
            self.status = self.Status.PENDING

        # Save the model instance to persist the changes
        if save:
            self.save(update_fields=['status'])

    @classmethod
    def mark_as_completed(cls, task_id):
        """
        Marks the task as completed and sets the completion date.
        """
        task = cls.objects.get(pk=task_id)
        task.is_manually_completed = True
        task.status = cls.Status.COMPLETED
        task.completion_date = timezone.now()
        task.save()

    def clean(self):
        super().clean()
        if self.start_date and self.due_date and self.start_date > self.due_date:
            raise ValidationError(_('Start date cannot be later than due date.'))

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to update the status before saving.
        """
        self.full_clean()
        self.update_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Title: {self.title}, Priority: {self.priority}, Status: {self.status}"

class Category(models.Model):
    """
    Represents a category for tasks.
    """
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_category')

    def __str__(self):
        return self.category_name

