import React from "react";

const WeatherWidget = ({ weatherData }) => {
  // Check if weatherData is undefined or null and handle it
  if (!weatherData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Weather Data</h2>
      <ul>
        {weatherData.map((data, index) => (
          <li key={index}>
            {" "}
            {/* Ensure each list item has a unique key */}
            {data.location}: {data.temperature}°C
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WeatherWidget;
