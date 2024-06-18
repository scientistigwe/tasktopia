from rest_framework import serializers
from .models import Task, UserTask, TaskCategory, TaskWeather, TaskForecast, TaskReport

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

# UserTask Serializer
class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = '__all__'

# TaskCategory Serializer
class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = '__all__'

# TaskWeather Serializer
class TaskWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWeather
        fields = '__all__'

# TaskForecast Serializer
class TaskForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskForecast
        fields = '__all__'

# TaskReport Serializer
class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReport
        fields = '__all__'
