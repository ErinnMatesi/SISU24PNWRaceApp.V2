import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import RegisterTeam from "./pages/RegisterTeam";
import RegisterRacer from "./pages/RegisterRacer";
import Dashboard from "./pages/Dashboard";
import Leaderboard from "./pages/Leaderboard";
import EditPanel from "./pages/EditPanel";

function App() {
  return (
    <Router>
      <nav className="p-4 bg-gray-100 flex gap-4">
        <Link to="/">Dashboard</Link>
        <Link to="/register-team">Register Team</Link>
        <Link to="/register-racer">Register Racer</Link>
        <Link to="/leaderboard">Leaderboard</Link>
        <Link to="/edit">Admin Edit</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/register-team" element={<RegisterTeam />} />
        <Route path="/register-racer" element={<RegisterRacer />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/edit" element={<EditPanel />} />
      </Routes>
    </Router>
  );
}

export default App;

