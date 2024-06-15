import React from "react";
import { Bar } from "react-chartjs-2";

const PrecipitationBarChart = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.timestamp),
    datasets: [
      {
        label: "Precipitation (mm)",
        data: data.map((item) => item.precipitation),
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
          text: "Precipitation (mm)",
        },
      },
      x: {
        title: {
          display: true,
          text: "Time",
        },
      },
    },
  };

  return (
    <div>
      <h3>Precipitation Bar Chart</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default PrecipitationBarChart;
