from rest_framework import serializers
from .models import Report, ReportDetail, ReportNotification, UserReport, ReportWeather, ReportForecast, ReportEventLog

# Report Serializer
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

# ReportDetail Serializer
class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDetail
        fields = '__all__'

# ReportNotification Serializer
class ReportNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportNotification
        fields = '__all__'

# UserReport Serializer
class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReport
        fields = '__all__'

# ReportWeather Serializer
class ReportWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportWeather
        fields = '__all__'

# ReportForecast Serializer
class ReportForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportForecast
        fields = '__all__'

# ReportEventLog Serializer
class ReportEventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportEventLog
        fields = '__all__'
