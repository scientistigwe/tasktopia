from django.contrib import admin
from .models import Category, Notification, Report, Weather, Forecast, EventLog
from accounts.models import User

# Register your models here.

admin.site.register(Category)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(Weather)
admin.site.register(Forecast)
admin.site.register(EventLog)
