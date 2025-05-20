import React, { useState } from "react";
import axios from "axios";

export default function BibNumberLookup({ onRacerFound }) {
    const [bibNumber, setBibNumber] = useState("");
    const [racer, setRacer] = useState(null);
    const [message, setMessage] = useState("");

    const handleKeyPress = async (e) => {
        if (e.key !== "Enter" || !bibNumber.trim()) return;

        try {
            // Step 1: Fetch racer
            const { data: racerData } = await axios.get(`/racers/bib/${bibNumber}`);

            setRacer(racerData);

            // Step 2: Attempt to fetch active trail
            let activeTrail = null;

            try {
                const { data } = await axios.get(`/active-trail/${racerData.racer_id}`);
                activeTrail = data;
            } catch (trailError) {
                if (trailError.response?.status !== 404) {
                    console.error("Error fetching active trail:", trailError);
                }
            }

            // Step 3: Set message
            const name = `${racerData.first_name} ${racerData.last_name}`;
            if (activeTrail?.trail_id) {
                setMessage(`${name} is currently on ${activeTrail.trail_name}`);
            } else {
                setMessage(`${name} is not currently on a trail.`);
            }

            // Step 4: Notify parent
            onRacerFound({
                id: racerData.racer_id,
                first_name: racerData.first_name,
                last_name: racerData.last_name,
                active_trail_id: activeTrail?.trail_id || null,
                active_trail_name: activeTrail?.trail_name || null
            });

        } catch (err) {
            console.error("Racer fetch failed:", err);
            setRacer(null);
            setMessage("❌ Racer not found or error retrieving data.");
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
            {message && <p className="text-sm text-gray-600">{message}</p>}
        </div>
    );
}
