import React from "react";
import { Scatter } from "react-chartjs-2";

const RealTimeTemperatureHumidityScatterPlot = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.timestamp),
    datasets: [
      {
        label: "Temperature vs. Humidity",
        data: data.map((item) => ({ x: item.temperature, y: item.humidity })),
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Humidity (%)",
        },
      },
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Temperature (°C)",
        },
      },
    },
  };

  return (
    <div>
      <h3>Real-Time Temperature vs. Humidity Scatter Plot</h3>
      <Scatter data={chartData} options={options} />
    </div>
  );
};

export default RealTimeTemperatureHumidityScatterPlot;
