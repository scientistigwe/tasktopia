import React from "react";
import { Link } from "react-router-dom";

const NavigationMenu = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/real-time-dashboard">Real-Time Dashboard</Link>
        </li>
        <li>
          <Link to="/forecast-dashboard">Forecast Dashboard</Link>
        </li>
        {/* Add more navigation links as needed */}
      </ul>
    </nav>
  );
};

export default NavigationMenu;
