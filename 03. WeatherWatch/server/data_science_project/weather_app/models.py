from django.db import models

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
