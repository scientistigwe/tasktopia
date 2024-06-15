import React, { useEffect, useState } from "react";

const ForecastDashboardPage = () => {
  const [forecast, setForecast] = useState([]);

  useEffect(() => {
    fetch("/api/weather-forecast/")
      .then((response) => response.json())
      .then((data) => setForecast(data));
  }, []);

  return (
    <div>
      <h2>Weather Forecast</h2>
      <ul>
        {forecast.map((item, index) => (
          <li key={index}>
            <p>Time: {new Date(item.forecast_time).toLocaleString()}</p>
            <p>Temperature: {item.temperature}°C</p>
            <p>Humidity: {item.humidity}%</p>
            <p>Wind Speed: {item.wind_speed} m/s</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ForecastDashboardPage;
