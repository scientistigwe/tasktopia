from django.db import models
from dashboard.models import Task, Category, Report, Weather, Forecast, EventLog
from accounts.models import User
from django.contrib.auth import get_user_model

# Simplify getting the default username
DEFAULT_USER_NAME = get_user_model().objects.first().first_name if get_user_model().objects.exists() else ''

class TaskRelationship(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    event_log = models.OneToOneField(EventLog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_relationships', default=DEFAULT_USER_NAME)

    def __str__(self):
        return f"{self.user.username}: {self.task.title}"

class TaskCategory(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task.title} ({self.category.name})"

class TaskWeather(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task.title} - {self.weather.condition}"

class TaskForecast(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    forecast = models.OneToOneField(Forecast, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task.title} - {self.forecast.forecast_condition}"

class TaskReport(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task.title} - {self.report.content}"
