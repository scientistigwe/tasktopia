import React from "react";
import { Bar } from "react-chartjs-2";

const SunriseSunsetTimesBarChart = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.date),
    datasets: [
      {
        label: "Sunrise Time",
        data: data.map((item) => item.sunrise_time),
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
      {
        label: "Sunset Time",
        data: data.map((item) => item.sunset_time),
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderColor: "rgba(255, 206, 86, 1)",
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
          text: "Time",
        },
      },
      x: {
        title: {
          display: true,
          text: "Date",
        },
      },
    },
  };

  return (
    <div>
      <h3>Sunrise and Sunset Times Bar Chart</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default SunriseSunsetTimesBarChart;
