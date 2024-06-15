import React from "react";
import Heatmap from "react-heatmap-grid";

const RainfallIntensityHeatmap = ({ data }) => {
  const xLabels = new Array(24).fill(0).map((_, i) => `${i}:00`);
  const yLabels = data.map((item) => item.date);
  const dataPoints = data.map((item) => item.rainfall_intensity);

  return (
    <div>
      <h3>Rainfall Intensity Heatmap</h3>
      <Heatmap
        xLabels={xLabels}
        yLabels={yLabels}
        data={dataPoints}
        xLabelWidth={60}
        cellStyle={(background, value, min, max, data, x, y) => ({
          background: `rgba(75,192,192,${1 - (max - value) / (max - min)})`,
          fontSize: "11px",
          color: "#444",
        })}
        cellRender={(value) => value && `${value.toFixed(2)} mm`}
        cellHeight={20}
        cellWidth={50}
      />
    </div>
  );
};

export default RainfallIntensityHeatmap;
