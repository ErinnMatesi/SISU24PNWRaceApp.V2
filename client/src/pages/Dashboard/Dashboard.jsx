import React from "react";
// import ActiveRunners from "../components/ActiveRunners";
import CheckInOut from "../../components/CheckInOut/CheckInOut.jsx";
import BonusPoints from "../../components/BonusPoints/BonusPoints.jsx";
import './Dashboard.css';

export default function Dashboard() {
    return (
        <div className="dashboard">
            <h1 className="title">Dashboard</h1>
            {/* <ActiveRunners /> */}
            <div className="dashboard-boxes">
                <CheckInOut />
                <BonusPoints />
            </div>
        </div>
    );
}
