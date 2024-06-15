import React from "react";

const WindDirectionCompassChart = ({ windDirection }) => {
  const getDirection = (angle) => {
    const directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
    const index = Math.round(angle / 45) % 8;
    return directions[index];
  };

  return (
    <div>
      <h3>Wind Direction Compass</h3>
      <p>{getDirection(windDirection)}</p>
    </div>
  );
};

export default WindDirectionCompassChart;
