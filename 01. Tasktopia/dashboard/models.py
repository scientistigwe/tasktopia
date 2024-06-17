from django.db import models
from django.contrib.auth.models import User

# Category Model.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Category: {self.category}")

# Task Model
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField
    due_date = models.DateField(max_length=50)
    priority = models.TextChoices
    status = models.TextChoices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='tasks')

    def __str__(self):
        return (f"Title: {self.title}, Description: {self.description}, Priority: {self.priority}, Status: {self.status}")


class Notification(models.Model):
  notification_id = models.AutoField(primary_key=True)
  message = models.TextField
  sent_at = models.DateTimeField
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
  task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications')


class Report(models.Model):
    report_id = models.AutoField(primary_key=True) 
    generated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')

    def __str__(self):
       return f"Content: {self.content}"


class Weather(models.Model):
    weather_id = models.AutoField(primary_key=True)
    current_date = models.DateTimeField
    forecast_date = models.DateTimeField
    condition = models.CharField(max_length=50)
    temperature = models.IntegerField
    current_location = models.CharField(max_length=50)
    event_location = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather')

class Forecast(models.Model):
  forecast_id = models.AutoField(primary_key=True)
  forecast_day = models.IntegerField
  forecast_condition = models.CharField(max_length=50)
  forecast_temperature = models.IntegerField
  forecast_location = models.CharField(max_length=50)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forecast')
  weather_id = models.OneToOneField(Weather, on_delete=models.CASCADE, related_name='forecasts')

  def __str__(self):
     return (f"Condition: {self.forecast_condition}, Forecast Location: {self.forecast_location}")


class Event(models.Model):
  eventlog_id = models.AutoField(primary_key=True)
  event = models.CharField(max_length=225) 
  event_time = models.DateTimeField
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
  task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='events')

  def __str__(self):
     return f""
