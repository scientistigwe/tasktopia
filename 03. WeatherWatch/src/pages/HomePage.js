// HomePage.js

import React from "react";
import WeatherWidget from "../components/WeatherWidget";

const HomePage = () => {
  return (
    <div className="home-page">
      <h1>Welcome to Weather Dashboard</h1>
      <WeatherWidget />
    </div>
  );
};

export default HomePage;
