import React from "react";
import ActiveRunners from "../components/ActiveRunners";
import CheckInOut from "../components/CheckInOut";
import BonusPoints from "../components/BonusPoints";

export default function Dashboard() {
    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
            <ActiveRunners />
            <div className="mt-8">
                <CheckInOut />
                <BonusPoints />
            </div>
        </div>
    );
}
