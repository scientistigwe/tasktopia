import React from "react";
import GaugeChart from "react-gauge-chart";

const HumidityGaugeChart = ({ humidity }) => {
  return (
    <div>
      <h3>Humidity Gauge Chart</h3>
      <GaugeChart
        id="humidity-gauge-chart"
        textColor="black"
        percent={humidity / 100}
      />
    </div>
  );
};

export default HumidityGaugeChart;
