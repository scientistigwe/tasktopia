const BASE_URL = "http://localhost:8000/";
const CURRENT_WEATHER_ENDPOINT = "current-weather/";
const FORECAST_ENDPOINT = "weather-forecast/";

export const fetchRealTimeWeatherData = async () => {
  try {
    const response = await fetch(`${BASE_URL}${CURRENT_WEATHER_ENDPOINT}`);
    if (!response.ok) {
      throw new Error("Failed to fetch real-time weather data");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching real-time weather data:", error);
    throw error;
  }
};

export const fetchForecastWeatherData = async () => {
  try {
    const response = await fetch(`${BASE_URL}${FORECAST_ENDPOINT}`);
    if (!response.ok) {
      throw new Error("Failed to fetch forecast weather data");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching forecast weather data:", error);
    throw error;
  }
};
