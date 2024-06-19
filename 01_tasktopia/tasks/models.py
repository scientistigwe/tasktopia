from django.db import models
from django.contrib.auth.models import User
from dashboard.models import UserProfile, Task, Category, Report, Weather, Forecast, EventLog

class UserTask(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    event_log = models.OneToOneField(EventLog, on_delete=models.CASCADE)

    def __str__(self):
        return f"UserTask: {self.task.title} assigned to {self.user_profile.user.username}"

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
    

class CurrentWeather(models.Model):
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=50)
    precipitation = models.FloatField()
    uv_index = models.FloatField(default=0)  # Added default value
    air_pressure = models.FloatField()
    visibility = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Current Weather"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.location} - {self.timestamp}"

class WeatherForecast(models.Model):
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=50)
    precipitation = models.FloatField()
    uv_index = models.FloatField(default=0)  # Added default value
    air_pressure = models.FloatField()
    visibility = models.FloatField()
    forecast_time = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Weather Forecasts"
        ordering = ['-forecast_time']

    def __str__(self):
        return f"{self.location} - {self.forecast_time}"

