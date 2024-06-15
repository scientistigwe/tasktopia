import React from "react";
import { Area } from "react-chartjs-2";

const CloudCoverAreaChart = ({ data }) => {
  const chartData = {
    labels: data.map((item) => item.forecast_time),
    datasets: [
      {
        label: "Cloud Cover (%)",
        data: data.map((item) => item.cloud_cover),
        fill: true,
        backgroundColor: "rgba(75,192,192,0.2)",
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
        beginAtZero: true,
        title: {
          display: true,
          text: "Cloud Cover (%)",
        },
      },
    },
  };

  return (
    <div>
      <h3>Cloud Cover Area Chart</h3>
      <Area data={chartData} options={options} />
    </div>
  );
};

export default CloudCoverAreaChart;
