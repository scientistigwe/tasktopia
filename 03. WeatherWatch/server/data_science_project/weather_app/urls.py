from django.contrib import admin
from django.urls import path
from weather_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('current-weather/', views.current_weather_view, name='current_weather'),
    path('weather-forecast/', views.weather_forecast_view, name='weather_forecast'),
]

# Add urlpatterns for other paths as needed
