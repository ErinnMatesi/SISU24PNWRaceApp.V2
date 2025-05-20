import React, { useState, useEffect } from "react";
import axios from "axios";

export default function BibNumberLookup({ onRacerFound }) {
    const [bibNumber, setBibNumber] = useState("");
    const [racer, setRacer] = useState(null);
    const [currentTrail, setCurrentTrail] = useState(null);
    const [message, setMessage] = useState("");

    const handleKeyPress = async (e) => {
        if (e.key === "Enter" && bibNumber.trim() !== "") {
            try {
                // Fetch racer details
                const racerResponse = await axios.get(`/racers/bib/${bibNumber}`);
                const racerData = racerResponse.data;

                // Fetch active trail entry (if any)
                const activeEntryResponse = await axios.get(`/active-trail/${bibNumber}`);
                const activeEntry = activeEntryResponse.data;

                // Set local state for display
                setRacer(racerData);
                
                // Set message based on active trail status
                if (activeEntry.trail_id) {
                    setCurrentTrail(activeEntry);
                    setMessage(
                        `${racerData.first_name} ${racerData.last_name} is currently on ${activeEntry.trail_name}`
                    );
                } else {
                    setCurrentTrail(null);
                    setMessage(
                        `${racerData.first_name} ${racerData.last_name} is not currently on a trail.`
                    );
                }

                // Inform parent component of found racer
                onRacerFound({
                    racer_id: racerData.id,
                    first_name: racerData.first_name,
                    last_name: racerData.last_name,
                    active_trail_id: activeEntry.trail_id || null,
                    active_trail_name: activeEntry.trail_name || null
                });

            } catch (error) {
                console.error(error);
                setMessage("❌ Racer not found or error retrieving data.");
                setRacer(null);
                setCurrentTrail(null);
            }
        }
    };

    return (
        <div className="mb-4">
            <input
                placeholder="Bib Number"
                value={bibNumber}
                onChange={(e) => setBibNumber(e.target.value)}
                onKeyPress={handleKeyPress}
                className="border rounded w-full p-2 mb-2"
            />
            {racer && <p>{racer.first_name} {racer.last_name}</p>}
            {message && <p className="text-sm text-gray-600">{message}</p>}
        </div>
    );
}
