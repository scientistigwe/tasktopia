import React from "react";
import { Bar } from "react-chartjs-2";

const AirPressureBarChart = ({ data }) => {
  const chartData = {
    labels: data.map((entry) => entry.timestamp),
    datasets: [
      {
        label: "Air Pressure (hPa)",
        data: data.map((entry) => entry.air_pressure),
        backgroundColor: "rgba(255, 159, 64, 0.2)",
        borderColor: "rgba(255, 159, 64, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    indexAxis: "x",
    scales: {
      x: {
        title: {
          display: true,
          text: "Timestamp",
        },
      },
      y: {
        title: {
          display: true,
          text: "Air Pressure (hPa)",
        },
      },
    },
  };

  return (
    <div>
      <h2>Air Pressure Bar Chart</h2>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default AirPressureBarChart;
