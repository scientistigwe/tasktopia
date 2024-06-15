// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import NavigationMenu from "./components/NavigationMenu";
import RealTimeDashboardPage from "./pages/RealTimeDashboardPage";
import ForecastDashboardPage from "./pages/ForecastDashboardPage";
import HomePage from "./pages/HomePage";
import ProfilePage from "./pages/ProfilePage";
import AlertsPage from "./pages/AlertsPage";
import ReportsPage from "./pages/ReportsPage";
import SettingsPage from "./pages/SettingsPage";

function App() {
  return (
    <Router>
      <div>
        <Header />
        <NavigationMenu />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/real-time-dashboard"
            element={<RealTimeDashboardPage />}
          />
          <Route
            path="/forecast-dashboard"
            element={<ForecastDashboardPage />}
          />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
