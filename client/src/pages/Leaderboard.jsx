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
  1: { name: "Snoquera Falls", distance: 3.75, elevation: 802, redFlag: 161 },
  2: { name: "Noble Knob", distance: 18.91, elevation: 4087, redFlag: 465 },
  3: { name: "Little Ranger Peak", distance: 12.65, elevation: 2872, redFlag: 402 },
  4: { name: "Dalles Falls", distance: 3.25, elevation: 480, redFlag: 120 },
  5: { name: "Little Ranger Lookout", distance: 9.10, elevation: 1618, redFlag: 295 },
  6: { name: "Goat Falls", distance: 9.85, elevation: 1298, redFlag: 285 },
  7: { name: "SISU Service", distance: 0.00, elevation: 0, redFlag: 60 }
};

const Leaderboard = () => {
  const [categoryData, setCategoryData] = useState({});
  const [trailData, setTrailData] = useState([]);

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 30000); // Refresh every 30 sec
    return () => clearInterval(interval);
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
    <div key={key} className="p-4 bg-white rounded shadow mb-6">
      <h2 className="text-lg font-semibold mb-2">{label}</h2>
      <ul className="text-sm">
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
      <div key={trail.trail_id} className="p-4 bg-yellow-50 rounded shadow mb-6">
        <h2 className="text-lg font-semibold mb-1">{info.name || `Trail #${trail.trail_id}`}</h2>
        <p className="text-xs text-gray-600 mb-1">
          Distance: {info.distance} mi | Elevation: {info.elevation} ft | Red Flag: {info.redFlag} min
        </p>
        <p className="text-xs text-gray-600 mb-2">
          Gold Remaining: {trail.first_ten_points} | Silver Remaining: {trail.second_ten_points}
        </p>
        <ul className="text-sm">
          {(trail.active_runners || []).map((runner) => {
            const startTime = new Date(runner.start_time);
            const minsOut = Math.floor((now - startTime) / 60000);
            const isOverTime = minsOut > (info.redFlag || 90);

            return (
              <li
                key={runner.racer_id}
                className={isOverTime ? "text-red-500 font-semibold" : ""}
              >
                {runner.first_name} {runner.last_name} — Out {minsOut} min
              </li>
            );
          })}
        </ul>
      </div>
    );
  };

  return (
    <div className="p-6 max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Category Ranking Boxes */}
      {categories.map(({ key, label }) => renderCategoryBox(key, label))}

      {/* Trail Boxes */}
      {trailData.map((trail) => renderTrailBox(trail))}
    </div>
  );
};

export default Leaderboard;
