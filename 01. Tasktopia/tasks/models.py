from django.db import models
from django.contrib.auth.models import User
from dashboard.models import UserProfile, Task, Category, Report, Weather, Forecast, EventLog

class UserTask(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)  # Assuming the model is named 'Task' in the same app
    event_log = models.OneToOneField(EventLog, on_delete=models.CASCADE)

    def __str__(self):
        return f"UserTask: {self.task.title} assigned to {self.user_profile.user.username}"

class TaskCategory(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)  # Assuming the model is named 'Task' in the same app
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Category: {self.category}"

class TaskWeather(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)  # Assuming the model is named 'Task' in the same app
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Weather: {self.weather.condition}"

class TaskForecast(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)  # Assuming the model is named 'Task' in the same app
    forecast = models.OneToOneField(Forecast, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Forecast: {self.forecast.forecast_condition}"

class TaskReport(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)  # Assuming the model is named 'Task' in the same app
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task: {self.task.title}, Report: {self.report.content}"
