from django.shortcuts import render
from django.http import JsonResponse
from weather_app.models import CurrentWeather, WeatherForecast

def current_weather_view(request):
    try:
        current_weather_data = CurrentWeather.objects.all().values('location', 'latitude', 'longitude',
                                                                   'temperature', 'humidity', 'wind_speed',
                                                                   'wind_direction', 'precipitation', 'uv_index',
                                                                   'air_pressure', 'visibility', 'timestamp')
        if current_weather_data.exists():
            return JsonResponse(list(current_weather_data), safe=False)
        else:
            return JsonResponse({'error': 'No current weather data available'}, status=404)
    except CurrentWeather.DoesNotExist:
        return JsonResponse({'error': 'Current weather data not found'}, status=404)


def weather_forecast_view(request):
    try:
        weather_forecast_data = WeatherForecast.objects.all().values('location', 'latitude', 'longitude',
                                                                     'temperature', 'humidity', 'wind_speed',
                                                                     'wind_direction', 'precipitation', 'uv_index',
                                                                     'air_pressure', 'visibility', 'forecast_time')
        if weather_forecast_data.exists():
            return JsonResponse(list(weather_forecast_data), safe=False)
        else:
            return JsonResponse({'error': 'No weather forecast data available'}, status=404)
    except WeatherForecast.DoesNotExist:
        return JsonResponse({'error': 'Weather forecast data not found'}, status=404)
