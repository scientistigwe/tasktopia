import React, { useState, useEffect } from "react";
import WeatherWidget from "../components/WeatherWidget";
import { fetchRealTimeWeatherData } from "../api/WeatherApi";

const RealTimeDashboardPage = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true); // Add a loading state

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchRealTimeWeatherData();
        setWeatherData(data);
        setLoading(false); // Set loading to false when data is fetched
      } catch (error) {
        console.error("Error fetching real-time weather data:", error);
        setLoading(false); // Ensure loading is set to false even if there is an error
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Real-Time Weather Dashboard</h1>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <WeatherWidget weatherData={weatherData} />
      )}
    </div>
  );
};

export default RealTimeDashboardPage;
