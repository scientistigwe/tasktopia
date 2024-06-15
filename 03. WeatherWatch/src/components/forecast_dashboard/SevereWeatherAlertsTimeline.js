import React from "react";
import Timeline from "react-calendar-timeline";

const SevereWeatherAlertsTimeline = ({ data }) => {
  const items = data.map((item) => ({
    id: item.id,
    group: item.weather_alert_type,
    title: item.weather_alert_type,
    start_time: new Date(item.start_time),
    end_time: new Date(item.end_time),
  }));

  const groups = [...new Set(data.map((item) => item.weather_alert_type))].map(
    (type, index) => ({
      id: index,
      title: type,
    })
  );

  const defaultTimeStart = new Date();
  defaultTimeStart.setHours(0, 0, 0, 0);

  const defaultTimeEnd = new Date();
  defaultTimeEnd.setHours(23, 59, 59, 999);

  const timelineProps = {
    groups,
    items,
    defaultTimeStart,
    defaultTimeEnd,
  };

  return (
    <div>
      <h3>Severe Weather Alerts Timeline</h3>
      <Timeline {...timelineProps} />
    </div>
  );
};

export default SevereWeatherAlertsTimeline;
