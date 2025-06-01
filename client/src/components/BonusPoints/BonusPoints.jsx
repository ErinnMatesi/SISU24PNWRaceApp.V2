import React, { useState, useEffect } from "react";
import axios from "axios";
import BibNumberLookup from "../BibNumberLookup/BibNumberLookup.jsx";
import './BonusPoints.css';

export default function BonusPoints() {
    const [racer, setRacer] = useState(null);
    const [bonusObjectiveID, setBonusObjectiveID] = useState("");
    const [bonusObjectives, setBonusObjectives] = useState([]);
    const [message, setMessage] = useState("");

    useEffect(() => {
        fetchBonusObjectives();
    }, []);

    const fetchBonusObjectives = async () => {
        try {
            const response = await axios.get("/bonus-objectives");
            setBonusObjectives(response.data);
        } catch (error) {
            console.error(error);
            setMessage("Failed to fetch bonus objectives.");
        }
    };

    const handleRacerFound = (foundRacer) => {
        console.log("Found racer in BonusPoints:", foundRacer);
        setRacer(foundRacer);
        setMessage(""); // Clear any old messages
    };

    const handleSubmit = async () => {
        if (!racer || !bonusObjectiveID) {
            setMessage("❌ Please select a racer and a bonus objective.");
            return;
        }

        try {
            const response = await axios.post("/raceentry/bonuspoints", {
                racer_id: racer.id,
                bonus_objective_id: bonusObjectiveID,
            });

            setMessage(response.data.message);
            setRacer(null);
            setBonusObjectiveID("");

        } catch (error) {
            console.error(error);
            if (error.response && error.response.data && error.response.data.error) {
                setMessage(`❌ ${error.response.data.error}`);
            } else {
                setMessage("❌ Failed to assign bonus points.");
            }
        }
    };

    return (
        <div className="bonus-container">
            <h2 className="bonus-header">Side Quests</h2>

            {/* Bib Number Lookup */}
            <BibNumberLookup onRacerFound={handleRacerFound} />

            {/* Bonus Objective Selection */}
            {racer && (
                <>
                    <select
                        value={bonusObjectiveID}
                        onChange={(e) => setBonusObjectiveID(e.target.value)}
                        className="border rounded w-full p-2 mb-4"
                    >
                        <option value="">Select Side Quest</option>
                        {bonusObjectives.map((objective) => (
                            <option key={objective.id} value={objective.id}>
                                {objective.description}
                            </option>

                        ))}
                    </select>

                    <button
                        onClick={handleSubmit}
                        className="submit-button"
                    >
                        Submit Points
                    </button>
                </>
            )}

            {/* Status Message */}
            {message && <p className="message">{message}</p>}
        </div>
    );
}
