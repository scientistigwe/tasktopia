from django.core.management.base import BaseCommand
from weather_app.models import CurrentWeather, WeatherForecast
import requests
from datetime import datetime

API_KEY = 'b5a9fa9b52af2d466adaeceb1f4aeb48'
BASE_URL = 'http://api.openweathermap.org/data/2.5'
GEOCODING_BASE_URL = 'http://api.openweathermap.org/geo/1.0/direct'
MAPS_BASE_URL = 'https://tile.openweathermap.org/map'

def build_params(*args, **kwargs):
    """Helper function to build params dictionary."""
    params = {'appid': API_KEY}
    for arg in args:
        params.update(arg)
    params.update(kwargs)
    return params

def fetch_data(api_url, params=None):
    """Fetches data from the given API URL with optional parameters."""
    if params is None:
        params = {}
    try:
        response = requests.get(api_url, params=build_params(params))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return None

def fetch_weather(endpoint, lat, lon):
    """Fetches weather data based on the endpoint type (e.g., current weather, forecast)."""
    params = {'lat': lat, 'lon': lon, 'units': 'metric'}
    return fetch_data(f'{BASE_URL}/{endpoint}', params)

def fetch_geocoding_data(city_name, state_code, country_code, limit=1):
    """Fetches geocoding data."""
    params = {'q': f'{city_name},{state_code},{country_code}', 'limit': limit}
    return fetch_data(GEOCODING_BASE_URL, params)

def get_weather_map(layer, z, x, y):
    """Gets a weather map URL."""
    url = f'{MAPS_BASE_URL}/{layer}/{z}/{x}/{y}.png'
    return url

def parse_weather_data(data, forecast=False):
    """Parses weather data into a structured format."""
    if forecast:
        forecast_weather = []
        for item in data['list']:
            forecast_entry = {
                'location': data['city']['name'],
                'latitude': data['city']['coord']['lat'],
                'longitude': data['city']['coord']['lon'],
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': item['wind']['deg'],
                'precipitation': item.get('rain', {}).get('1h', 0),
                'uv_index': 0,  # Placeholder as forecast API does not provide UV index
                'air_pressure': item['main']['pressure'],
                'visibility': item['visibility'],
                'timestamp': datetime.fromtimestamp(item['dt']),
                'forecast_time': datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            }
            forecast_weather.append(forecast_entry)
        return forecast_weather
    else:
        weather = {
            'location': data['name'],
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind']['deg'],
            'precipitation': data.get('rain', {}).get('1h', 0),
            'uv_index': 0,  # Placeholder as current weather API does not provide UV index
            'air_pressure': data['main']['pressure'],
            'visibility': data['visibility'],
            'timestamp': datetime.fromtimestamp(data['dt'])
        }
        return weather

class Command(BaseCommand):
    help = 'Fetch and store weather data'

    def handle(self, *args, **kwargs):
        location = 'London'
        lat, lon = 51.5074, -0.1278

        # Fetch and parse current weather
        current_data = fetch_weather('weather', lat, lon)
        if current_data:
            current_weather = parse_weather_data(current_data)
            CurrentWeather.objects.create(**current_weather)
        else:
            self.stderr.write("Failed to fetch current weather data")

        # Fetch and parse weather forecast
        forecast_data = fetch_weather('forecast', lat, lon)
        if forecast_data:
            forecast_weather = parse_weather_data(forecast_data, forecast=True)
            if isinstance(forecast_weather, list):
                for forecast in forecast_weather:
                    WeatherForecast.objects.create(**forecast)
            else:
                self.stderr.write("Failed to parse forecast data: Invalid format")
        else:
            self.stderr.write("Failed to fetch forecast data")

        # Fetch geocoding data
        city_name, state_code, country_code = 'London', '', 'GB'
        geocoding_data = fetch_geocoding_data(city_name, state_code, country_code)
        if geocoding_data:
            self.stdout.write(f'Geocoding Data: {geocoding_data}')
        else:
            self.stderr.write("Failed to fetch geocoding data")

        # Get weather map URL
        layer, z, x, y = 'temp_new', 10, 512, 512
        weather_map_url = get_weather_map(layer, z, x, y)
        self.stdout.write(f'Weather Map URL: {weather_map_url}')

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored weather data'))
