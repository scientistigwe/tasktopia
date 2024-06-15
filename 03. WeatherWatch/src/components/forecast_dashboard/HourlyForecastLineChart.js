import React from "react";
import { Line } from "react-chartjs-2";

const HourlyForecastLineChart = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.forecast_time),
    datasets: [
      {
        label: "Hourly Forecast Temperature (°C)",
        data: data.map((item) => item.temperature),
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
          text: "Time",
        },
      },
      y: {
        title: {
          display: true,
          text: "Temperature (°C)",
        },
      },
    },
  };

  return (
    <div>
      <h3>Hourly Forecast Line Chart</h3>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default HourlyForecastLineChart;
