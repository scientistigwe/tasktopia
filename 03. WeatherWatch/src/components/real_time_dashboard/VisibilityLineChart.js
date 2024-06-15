import React from "react";
import { Line } from "react-chartjs-2";

const VisibilityLineChart = ({ data }) => {
  const chartData = {
    labels: data.map((entry) => entry.timestamp),
    datasets: [
      {
        label: "Visibility",
        data: data.map((entry) => entry.visibility),
        fill: false,
        borderColor: "rgba(255, 206, 86, 1)",
        tension: 0.1,
      },
    ],
  };

  return (
    <div>
      <h2>Visibility Line Chart</h2>
      <Line data={chartData} />
    </div>
  );
};

export default VisibilityLineChart;
