import React, { useState, useEffect } from "react";
import axios from "axios";

const RegisterRacer = () => {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    gender: "Male",
    age: "",
    bib_number: "",
    division: "24hr individual",
    team_id: "", // FK from teams
  });
  const [teams, setTeams] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Fetch teams for dropdown
    const fetchTeams = async () => {
      try {
        const res = await axios.get("/teams");
        setTeams(res.data);
      } catch (err) {
        console.error("Error fetching teams:", err);
      }
    };
    fetchTeams();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Ensure empty team_id is converted to null
    const cleanedFormData = {
      ...formData,
      team_id: formData.team_id === "" ? null : formData.team_id,
    };

    try {
      await axios.post("/racers", cleanedFormData);
      setMessage("✅ Racer registered successfully!");
      setFormData({
        first_name: "",
        last_name: "",
        gender: "Male",
        age: "",
        bib_number: "",
        division: "24hr individual",
        team_id: "",
      });
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
      <h1 className="text-2xl font-bold mb-4">Register a New Racer</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          value={formData.first_name}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          value={formData.last_name}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        >
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Nonbinary">Nonbinary</option>
        </select>
        <input
          type="number"
          name="age"
          placeholder="Age"
          value={formData.age}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        />
        <input
          type="number"
          name="bib_number"
          placeholder="Bib Number"
          value={formData.bib_number}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        />
        <select
          name="division"
          value={formData.division}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        >
          <option value="24hr individual">24hr individual</option>
          <option value="24hr team">24hr team</option>
          <option value="100 milers">100 milers</option>
        </select>
        <select
          name="team_id"
          value={formData.team_id}
          onChange={handleChange}
          className="w-full p-2 border rounded"
        >
          <option value="">No Team (Individual)</option>
          {teams.map((team) => (
            <option key={team.id} value={team.id}>
              {team.team_name}
            </option>
          ))}
        </select>
        <button type="submit" className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
          Register Racer
        </button>
      </form>

      {message && <p className="mt-4">{message}</p>}
    </div>
  );
};

export default RegisterRacer;
