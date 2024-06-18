from django.contrib import admin
from tasks.models import UserTask, TaskCategory, TaskWeather, TaskForecast, TaskReport

admin.site.register(UserTask)
admin.site.register(TaskCategory)
admin.site.register(TaskWeather)
admin.site.register(TaskForecast)
admin.site.register(TaskReport)
