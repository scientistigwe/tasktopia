import React from "react";
import { Doughnut } from "react-chartjs-2";

const UVIndexDonutChart = ({ uvIndex }) => {
  const chartData = {
    labels: ["UV Index"],
    datasets: [
      {
        label: "UV Index",
        data: [uvIndex],
        backgroundColor: ["#FF6384"],
        hoverBackgroundColor: ["#FF6384"],
      },
    ],
  };

  return (
    <div>
      <h3>UV Index Donut Chart</h3>
      <Doughnut data={chartData} />
    </div>
  );
};

export default UVIndexDonutChart;
