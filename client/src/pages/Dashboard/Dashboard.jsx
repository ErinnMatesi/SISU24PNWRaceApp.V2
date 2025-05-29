import React from "react";
// import ActiveRunners from "../components/ActiveRunners";
import CheckInOut from "../../components/CheckInOut/CheckInOut.jsx";
import BonusPoints from "../../components/BonusPoints/BonusPoints.jsx";
import './Dashboard.css';

export default function Dashboard() {
    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
            {/* <ActiveRunners /> */}
            <div className="mt-8">
                <CheckInOut />
                <BonusPoints />
            </div>
        </div>
    );
}
