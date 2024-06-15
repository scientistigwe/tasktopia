import React from "react";
import { Radar } from "react-chartjs-2";

const WindSpeedRadarChart = ({ data }) => {
  const chartData = {
    labels: ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    datasets: [
      {
        label: "Wind Speed (m/s)",
        data: data.map((item) => item.wind_speed),
        fill: true,
        backgroundColor: "rgba(75,192,192,0.2)",
        borderColor: "rgba(75,192,192,1)",
        pointBackgroundColor: "rgba(75,192,192,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(75,192,192,1)",
      },
    ],
  };

  const options = {
    scales: {
      r: {
        angleLines: {
          display: true,
        },
        suggestedMin: 0,
        suggestedMax: 10,
      },
    },
  };

  return (
    <div>
      <h3>Wind Speed Radar Chart</h3>
      <Radar data={chartData} options={options} />
    </div>
  );
};

export default WindSpeedRadarChart;
