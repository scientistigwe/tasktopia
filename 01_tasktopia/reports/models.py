from django.db import models
from django.contrib.auth.models import User
from dashboard.models import UserProfile, Task, Category, Notification, Report, Weather, Forecast, EventLog

class ReportDetail(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)  # Assuming task app is named 'task'
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report for {self.task.title} by {self.user_profile.user.username}"

class ReportNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Report Notification: {self.notification.message} - {self.report}"

class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user.username}, Report: {self.report}"
    
class ReportWeather(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report: {self.report.content}, Weather: {self.weather.condition}"

class ReportForecast(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    forecast = models.OneToOneField(Forecast, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report: {self.report.content}, Forecast: {self.forecast.forecast_condition}"

class ReportEventLog(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    event_log = models.OneToOneField(EventLog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report: {self.report.content}, Event Log: {self.event_log.event}"
