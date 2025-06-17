import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ActiveRunners.css";

export default function ActiveRunners() {
    const [runners, setRunners] = useState([]);

    useEffect(() => {
        fetchActiveRunners();
    }, []);

     const fetchActiveRunners = async () => {
        try {
            const { data } = await axios.get("/active-runners");
            setRunners(data);
        } catch (err) {
            console.error(err);
        }
    };

    const formatDuration = (start) => {
        const diffMs = Date.now() - new Date(start).getTime();
        const hours = Math.floor(diffMs / 3600000);
        const minutes = Math.floor(diffMs / 60000) % 60;
        return `${hours}h ${minutes}m`;
    };

    return (
        <div className="active-runners-container">
            <h2>Active Runners</h2>
            <ul className="active-runners-list">
                {runners.map((runner) => (
                    <li key={runner.racer_id}>
                        #{runner.bib_number} - {runner.first_name} {runner.last_name} - {runner.trail_name} - {formatDuration(runner.start_time)}
                    </li>
                ))}
            </ul>
        </div>
    );
}
