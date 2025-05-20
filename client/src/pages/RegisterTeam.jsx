import React, { useState } from "react";
import axios from "axios";

const RegisterTeam = () => {
  const [teamName, setTeamName] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post("/teams", { team_name: teamName });
      setMessage("✅ Team registered successfully!");
      setTeamName(""); // Clear form
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data && err.response.data.error) {
        setMessage(`❌ ${err.response.data.error}`);
      } else {
        setMessage("❌ Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Register a New Team</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Team Name"
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Register Team
        </button>
      </form>

      {message && <p className="mt-4">{message}</p>}
    </div>
  );
};

export default RegisterTeam;
