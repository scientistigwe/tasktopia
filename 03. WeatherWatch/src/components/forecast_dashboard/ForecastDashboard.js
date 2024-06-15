import React, { useEffect, useState } from "react";
import { fetchForecastWeatherData } from "./api"; // Adjust the path based on your project structure
import {
  HourlyForecastLineChart,
  WeatherConditionPieChart,
  HeatmapTemperatureOverTime,
  CloudCoverAreaChart,
  HistoricalWeatherTrendsLineChart,
  SunriseSunsetTimesBarChart,
  FeelsLikeTemperatureLineChart,
  SevereWeatherAlertsTimeline,
  RainfallIntensityHeatmap,
} from "./forecast_dashboard"; // Import specific components

const ForecastDashboardPage = () => {
  const [forecastWeatherData, setForecastWeatherData] = useState(null);

  useEffect(() => {
    const fetchForecastData = async () => {
      try {
        const data = await fetchForecastWeatherData();
        setForecastWeatherData(data);
      } catch (error) {
        console.error("Error fetching forecast weather data:", error);
      }
    };

    fetchForecastData();
  }, []);

  return (
    <div>
      <h1>Forecast Dashboard</h1>
      {forecastWeatherData && (
        <>
          <HourlyForecastLineChart data={forecastWeatherData.hourlyForecast} />
          <WeatherConditionPieChart
            data={forecastWeatherData.weatherCondition}
          />
          <HeatmapTemperatureOverTime
            data={forecastWeatherData.temperatureHeatmap}
          />
          <CloudCoverAreaChart data={forecastWeatherData.cloudCoverData} />
          <HistoricalWeatherTrendsLineChart
            data={forecastWeatherData.historicalWeatherTrends}
          />
          <SunriseSunsetTimesBarChart
            data={forecastWeatherData.sunriseSunsetTimes}
          />
          <FeelsLikeTemperatureLineChart
            data={forecastWeatherData.feelsLikeTemperature}
          />
          <SevereWeatherAlertsTimeline
            data={forecastWeatherData.severeWeatherAlerts}
          />
          <RainfallIntensityHeatmap
            data={forecastWeatherData.rainfallIntensity}
          />
        </>
      )}
    </div>
  );
};

export default ForecastDashboardPage;
