from django.db import models
from accounts.models import UserProfile

class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'High'
        MEDIUM = 'Medium'
        LOW = 'Low'

    class Status(models.TextChoices):
        PENDING = 'Pending'
        COMPLETED = 'Completed'
        OVERDUE = 'Overdue'

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_tasks')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_tasks')

    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Priority: {self.priority}, Status: {self.status}"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Category: {self.category}"

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_notifications')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_notifications')

    def __str__(self):
        return f"Message: {self.message}"

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_reports')

    def __str__(self):
        return f"Content: {self.content}"

class Weather(models.Model):
    weather_id = models.AutoField(primary_key=True)
    current_date = models.DateTimeField(auto_now_add=True)
    forecast_date = models.DateTimeField()
    condition = models.CharField(max_length=50)
    temperature = models.IntegerField()
    current_location = models.CharField(max_length=50)
    event_location = models.CharField(max_length=50)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_weather')

    def __str__(self):
        return f"Condition: {self.condition}, Current Location: {self.current_location}, Event Location: {self.event_location}"

class Forecast(models.Model):
    forecast_id = models.AutoField(primary_key=True)
    forecast_day = models.DateField()
    forecast_condition = models.CharField(max_length=50)
    forecast_temperature = models.IntegerField()
    forecast_location = models.CharField(max_length=50)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_forecasts')
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE, related_name='forecast')

    def __str__(self):
        return f"Forecast Condition: {self.forecast_condition}, Forecast Location: {self.forecast_location}"

class EventLog(models.Model):
    eventlog_id = models.AutoField(primary_key=True)
    event = models.CharField(max_length=225)
    event_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_event_logs')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_event_logs')

    def __str__(self):
        return f"Event: {self.event}"
