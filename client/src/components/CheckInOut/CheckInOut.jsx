import React, { useState, useEffect } from "react";
import axios from "axios";
import BibNumberLookup from "../BibNumberLookup/BibNumberLookup.jsx";
import './CheckInOut.css';

export default function CheckInOut() {
    const [racer, setRacer] = useState(null);
    const [trails, setTrails] = useState([]);
    const [trailID, setTrailID] = useState("");
    const [firstTen, setFirstTen] = useState(false);
    const [secondTen, setSecondTen] = useState(false);
    const [message, setMessage] = useState("");
    const [isCheckingIn, setIsCheckingIn] = useState(false);

    useEffect(() => {
        fetchTrails();
    }, []);

    const fetchTrails = async () => {
        try {
            const response = await axios.get("/trails");
            setTrails(response.data);
        } catch (error) {
            console.error(error);
            setMessage("❌ Failed to fetch trails.");
        }
    };

    const handleRacerFound = (foundRacer) => {
        setRacer(foundRacer);
        setIsCheckingIn(!!foundRacer.active_trail_id);
        setTrailID(foundRacer.active_trail_id || "");
    };

    const handleCheckOut = async () => {
        if (!racer || !trailID) {
            setMessage("❌ Please select a trail before checking out.");
            return;
        }

        console.log("Attempting checkout with:", {
            racer_id: racer.id,
            trail_id: Number(trailID)
        });

        try {
            await axios.post("/raceentry/checkout", {
                racer_id: racer.id,
                trail_id: trailID,
            });
            setMessage(`✅ ${racer.first_name} checked out successfully!`);
            setRacer(null);
            setTrailID("");
        } catch (error) {
            console.error(error);
            setMessage("❌ Failed to check out racer.");
        }
    };

    const handleCheckIn = async () => {
        if (!racer || !trailID) {
            setMessage("❌ Please select a trail before checking in.");
            return;
        }

        try {
            await axios.put(`/raceentry/checkin/${racer.id}`, {
                racer_id: racer.id,
                trail_id: trailID,
                first_ten: firstTen,
                second_ten: secondTen,
            });
            setMessage(`✅ ${racer.first_name} checked in successfully!`);
            setRacer(null);
            setTrailID("");
            setFirstTen(false);
            setSecondTen(false);
        } catch (error) {
            console.error(error);
            setMessage("❌ Failed to check in racer.");
        }
    };

    return (
        <div className="checkinout-container">
            <h2 className="checkinout-header">Check In / Out</h2>
            <BibNumberLookup onRacerFound={handleRacerFound} />

            {/* Check Out Form */}
            {!isCheckingIn && racer && (
                <>
                    <select
                        value={trailID}
                        onChange={(e) => setTrailID(e.target.value)}
                        className="trail-select"
                    >
                        <option value="">Select Trail</option>
                        {trails.map((trail) => (
                        <option
                            key={trail.id}
                            value={trail.id}
                            style={{ backgroundColor: trail.color || "white", color: "black" }}
                        >
                            {trail.name}
                        </option>
                        ))}
                    </select>
                    <button onClick={handleCheckOut} className="checkout-button">
                        Check Out On Trail
                    </button>
                </>
            )}

            {/* Check In Form */}
            {isCheckingIn && racer && (
                <>
                    <div className="bonus-select">
                        <label className="gold-bonus">Gold Bonus</label>
                        <input
                            type="checkbox"
                            checked={firstTen}
                            onChange={(e) => {
                                setFirstTen(e.target.checked);
                                if (e.target.checked) setSecondTen(false);
                            }}
                            className="checkbox"
                        />
                    </div>

                    <div className="bonus-select">
                        <label className="silver-bonus">Silver Bonus</label>
                        <input
                            type="checkbox"
                            checked={secondTen}
                            onChange={(e) => {
                                setSecondTen(e.target.checked);
                                if (e.target.checked) setFirstTen(false);
                            }}
                            className="checkbox"
                        />
                    </div>

                    <button onClick={handleCheckIn} className="checkin-button">
                        Check In From Trail
                    </button>
                </>
            )}

            {message && <p className="message">{message}</p>}
        </div>
    );
}
