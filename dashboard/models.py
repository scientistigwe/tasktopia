from django.db import models
from django.utils import timezone
from accounts.models import User
from django.conf import settings

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_category')

    def __str__(self):
        return self.category_name

class Task(models.Model):
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
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_tasks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_tasks')

    def __str__(self):
        return f"Title: {self.title}, Priority: {self.priority}, Status: {self.status}"

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notifications')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_notifications')

    def __str__(self):
        return f"Message: {self.message}"

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reports')

    def __str__(self):
        return f"Generated at: {self.generated_at}"

class Weather(models.Model):
    weather_id = models.AutoField(primary_key=True)
    current_date = models.DateTimeField(auto_now_add=True)
    forecast_date = models.DateTimeField()
    condition = models.CharField(max_length=50)
    temperature = models.IntegerField()
    current_location = models.CharField(max_length=50)
    event_location = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_weather')

    def __str__(self):
        return f"Condition: {self.condition}, Current Location: {self.current_location}, Event Location: {self.event_location}"

class Forecast(models.Model):
    forecast_id = models.AutoField(primary_key=True)
    forecast_day = models.DateField()
    forecast_condition = models.CharField(max_length=50)
    forecast_temperature = models.IntegerField()
    forecast_location = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_forecast')
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE, related_name='forecast')

    def __str__(self):
        return f"Forecast Condition: {self.forecast_condition}, Forecast Location: {self.forecast_location}"

class EventLog(models.Model):
    eventlog_id = models.AutoField(primary_key=True)
    event = models.CharField(max_length=225)
    event_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_eventlog')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_event_logs')

    def __str__(self):
        return f"Event: {self.event}"
