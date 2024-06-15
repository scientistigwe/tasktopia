from rest_framework import serializers
from .models import CurrentWeather, WeatherForecast

class CurrentWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentWeather
        fields = '__all__'  # Adjust fields based on your model

class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = '__all__'  # Adjust fields based on your model
