from django.db import models
from dashboard.models import Task, Category, Report, Weather, Forecast, EventLog
from accounts.models import User
from django.contrib.auth import get_user_model

def get_default_username():
    first_user = get_user_model().objects.first()
    if first_user:
        return first_user.first_name
    return ''  # Default to an empty string if no user exists

class TaskRelationship(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    event_log = models.OneToOneField(EventLog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_relationships', default=get_default_username)

    def __str__(self):
        return f"UserTask: {self.task.title} assigned to {self.user.username}"
class TaskCategory(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Category: {self.category.name}"

class TaskWeather(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Weather: {self.weather.condition}"

class TaskForecast(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    forecast = models.OneToOneField(Forecast, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Forecast: {self.forecast.forecast_condition}"

class TaskReport(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Report: {self.report.content}"
