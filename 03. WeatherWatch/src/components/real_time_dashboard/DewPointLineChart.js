import React from "react";
import { Line } from "react-chartjs-2";

const DewPointLineChart = ({ data }) => {
  const chartData = {
    labels: data.map((entry) => entry.timestamp),
    datasets: [
      {
        label: "Dew Point (°C)",
        data: data.map((entry) => entry.dew_point),
        fill: false,
        borderColor: "rgba(153, 102, 255, 1)",
        tension: 0.1,
      },
    ],
  };

  return (
    <div>
      <h2>Dew Point Line Chart</h2>
      <Line data={chartData} />
    </div>
  );
};

export default DewPointLineChart;
