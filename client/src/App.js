import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import './App.css';

import RegisterTeam from "./pages/RegisterTeam";
import RegisterRacer from "./pages/RegisterRacer";
import Dashboard from "./pages/Dashboard/Dashboard.jsx";
import Leaderboard from "./pages/Leaderboard/Leaderboard.jsx";
import EditPanel from "./pages/EditPanel/EditPanel.jsx";

function App() {
  const [bgClass, setBgClass] = useState("day");

  useEffect(() => {
    const hour = new Date().getHours();

    if ((hour >= 4 && hour < 6) || (hour >= 20 && hour < 22)) {
      setBgClass("evening");
    } else if (hour >= 6 && hour < 20) {
      setBgClass("day");
    } else {
      setBgClass("night");
    }
  }, []);

  return (
    <div className={`app-container ${bgClass}`}>
      <Router>
        <nav>
          <ul>
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/leaderboard">Leaderboard</Link></li>
            <li><Link to="/register-team">Register Team</Link></li>
            <li><Link to="/register-racer">Register Racer</Link></li>
            <li><Link to="/edit">Admin Edit</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/register-team" element={<RegisterTeam />} />
          <Route path="/register-racer" element={<RegisterRacer />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/edit" element={<EditPanel />} />
        </Routes>
      </Router>
    </div>
    
  );
}

export default App;

