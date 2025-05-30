import React, { useEffect, useState } from "react";
import axios from "axios";
import './Leaderboard.css';

const categories = [
  { key: "male_24hr", label: "Male 24HR" },
  { key: "female_24hr", label: "Female 24HR" },
  { key: "teams_24hr", label: "24HR Teams" },
  { key: "100miler", label: "100 Milers" }
];

const trailInfo = {
  1: { name: "Snoquera Falls", header: "/assets/images/headers/SnoqueraHeader.png", distance: 3.75, elevation: 802, redFlag: 161 },
  2: { name: "Noble Knob", header: "/assets/images/headers/NobleHeader.png", distance: 18.91, elevation: 4087, redFlag: 465 },
  3: { name: "Little Ranger Peak", header: "/assets/images/headers/LRPHeader.png", distance: 12.65, elevation: 2872, redFlag: 402 },
  4: { name: "Dalles Falls", header: "/assets/images/headers/DallesHeader.png", distance: 3.25, elevation: 480, redFlag: 120 },
  5: { name: "Little Ranger Lookout", header: "/assets/images/headers/LRLHeader.png", distance: 9.10, elevation: 1618, redFlag: 295 },
  6: { name: "Goat Falls", header: "/assets/images/headers/GoatHeader.png", distance: 9.85, elevation: 1298, redFlag: 285 },
  7: { name: "SISU Service", header: "/assets/images/headers/LeaderHeader.png", distance: 0.00, elevation: 0, redFlag: 60 }
};

const Leaderboard = () => {
  const [categoryData, setCategoryData] = useState({});
  const [trailData, setTrailData] = useState([]);
  const [bgClass, setBgClass] = useState("day");

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 30000); // Refresh every 30 sec
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour >= 6 && hour < 17) setBgClass("day");
    else if (hour >= 17 && hour < 21) setBgClass("evening");
    else setBgClass("night");
  }, []);

  const fetchAllData = async () => {
    try {
      const catResults = {};
      for (const { key } of categories) {
        const res = await axios.get(`/leaderboard/category/${key}`);
        catResults[key] = res.data;
      }
      setCategoryData(catResults);

      const trailRes = await axios.get("/leaderboard/trails");
      setTrailData(trailRes.data);
    } catch (err) {
      console.error("Failed to fetch leaderboard data:", err);
    }
  };

  const renderCategoryBox = (key, label) => (
    <div key={key} className="category-box">
      <h2 className="category-header">{label}</h2>
      <ul>
        {(categoryData[key] || []).map((racer, index) => (
          <li key={racer.id}>
            {index + 1}. {racer.first_name} {racer.last_name} — {racer.total_points} pts
          </li>
        ))}
      </ul>
    </div>
  );

  const renderTrailBox = (trail) => {
    const info = trailInfo[trail.trail_id] || {};
    const now = new Date();

    return (
        <div key={trail.trail_id} className="trail-box">
          <div
            className="trail-header"
            style={{ backgroundImage: `url(${info.header})` }}
          >
            <h2>{info.name}</h2>
            <p>{info.distance} mi • {info.elevation} ft</p>
          </div>
          <div className="trail-content">
            <p>
              Gold Remaining: {trail.first_ten_points} | Silver Remaining: {trail.second_ten_points}
            </p>
            <ul>
              {(trail.active_runners || []).map((runner) => {
                const startTime = new Date(runner.start_time);
                const minsOut = Math.floor((now - startTime) / 60000);
                const isOverTime = minsOut > (info.redFlag || 90);

                return (
                  <li
                    key={runner.racer_id}
                    className={isOverTime ? "overtime" : ""}
                  >
                    {runner.first_name} {runner.last_name} — Out {minsOut} min
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
    );
  };

  return (
    <div className={`leaderboard-container ${bgClass}`}>
      <div className="category-section">
        <div className="category-boxes">
          {categories.map(({ key, label }) => renderCategoryBox(key, label))}
        </div>
      </div>

      <div className="trail-section">
        {trailData.map((trail) => renderTrailBox(trail))}
      </div>
    </div>
  );
};

export default Leaderboard;
