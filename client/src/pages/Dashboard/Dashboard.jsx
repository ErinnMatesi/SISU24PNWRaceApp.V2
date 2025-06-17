import React from "react";
import ActiveRunners from "../../components/ActiveRunners/ActiveRunners.jsx";
import CheckInOut from "../../components/CheckInOut/CheckInOut.jsx";
import BonusPoints from "../../components/BonusPoints/BonusPoints.jsx";
import './Dashboard.css';

export default function Dashboard() {
    return (
        <div className="dashboard">
            <h1 className="title">Dashboard</h1>
            <div className="dashboard-boxes">
                <CheckInOut />
                <BonusPoints />
                <ActiveRunners />
            </div>
        </div>
    );
}
