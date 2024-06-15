import React from "react";
import { Line } from "react-chartjs-2";

const FeelsLikeTemperatureLineChart = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.date),
    datasets: [
      {
        label: "Feels Like Temperature (°C)",
        data: data.map((item) => item.feels_like_temperature),
        fill: false,
        borderColor: "rgba(75,192,192,1)",
        tension: 0.1,
      },
    ],
  };

  const options = {
    scales: {
      x: {
        title: {
          display: true,
          text: "Date",
        },
      },
      y: {
        title: {
          display: true,
          text: "Feels Like Temperature (°C)",
        },
      },
    },
  };

  return (
    <div>
      <h3>Feels Like Temperature Line Chart</h3>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default FeelsLikeTemperatureLineChart;
