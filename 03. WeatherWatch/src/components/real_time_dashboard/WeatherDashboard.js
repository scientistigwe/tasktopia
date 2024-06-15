import React, { useEffect, useState } from "react";
import { fetchRealTimeWeatherData, fetchForecastWeatherData } from "./api"; // Adjust the path based on your project structure
import {
  TemperatureLineChart,
  HumidityGaugeChart,
  WindSpeedRadarChart,
  PrecipitationBarChart,
  UVIndexDonutChart,
  WindDirectionCompassChart,
  RealTimeTemperatureHumidityScatterPlot,
  VisibilityLineChart,
  DewPointLineChart,
  AirPressureBarChart,
} from "./real_time_dashboard"; // Import specific components

const RealTimeDashboardPage = () => {
  const [realTimeWeatherData, setRealTimeWeatherData] = useState(null);

  useEffect(() => {
    const fetchRealTimeData = async () => {
      try {
        const data = await fetchRealTimeWeatherData();
        setRealTimeWeatherData(data);
      } catch (error) {
        console.error("Error fetching real-time weather data:", error);
      }
    };

    fetchRealTimeData();
  }, []);

  return (
    <div>
      <h1>Real-Time Weather Dashboard</h1>
      {realTimeWeatherData && (
        <>
          <TemperatureLineChart data={realTimeWeatherData} />
          <HumidityGaugeChart humidity={realTimeWeatherData.currentHumidity} />
          <WindSpeedRadarChart data={realTimeWeatherData.windSpeedData} />
          <PrecipitationBarChart data={realTimeWeatherData.precipitationData} />
          <UVIndexDonutChart uvIndex={realTimeWeatherData.uvIndexData} />
          <WindDirectionCompassChart
            windDirection={realTimeWeatherData.windDirectionData}
          />
          <RealTimeTemperatureHumidityScatterPlot
            data={realTimeWeatherData.temperatureData}
          />
          <VisibilityLineChart data={realTimeWeatherData.visibilityData} />
          <DewPointLineChart data={realTimeWeatherData.dewPointData} />
          <AirPressureBarChart data={realTimeWeatherData.airPressureData} />
        </>
      )}
    </div>
  );
};

export default RealTimeDashboardPage;
