from django.contrib import admin
from reports.models import ReportDetail, ReportNotification, UserReport, ReportWeather, ReportForecast, ReportEventLog

admin.site.register(ReportDetail)
admin.site.register(ReportNotification)
admin.site.register(UserReport)
admin.site.register(ReportWeather)
admin.site.register(ReportForecast)
admin.site.register(ReportEventLog)
