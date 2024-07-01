from django.db import models
from dashboard.models import Task, Category, Notification, Report, Weather, Forecast, EventLog
from accounts.models import User
from django.db import models

class ReportDetail(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report for {self.task.title} by {self.report.reported_by.username}"

class ReportNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Report Notification: {self.notification.message} - {self.report}"

class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f'Report by {self.user.username}'

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
