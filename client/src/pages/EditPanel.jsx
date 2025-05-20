import React, { useState } from "react";
import PasswordGate from "../components/PasswordGate";

const EditPanel = () => {
  const [activeTab, setActiveTab] = useState("racers");

  const renderContent = () => {
    switch (activeTab) {
      case "racers":
        return <div>🔧 Racer editing coming soon...</div>;
      case "teams":
        return <div>🔧 Team editing coming soon...</div>;
      case "entries":
        return <div>🔧 Race entry editing coming soon...</div>;
      default:
        return null;
    }
  };

  return (
    <PasswordGate>
      <div className="p-6 max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Edit Panel</h1>

        <div className="flex space-x-4 mb-6">
          <button
            className={`px-4 py-2 rounded ${activeTab === "racers" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
            onClick={() => setActiveTab("racers")}
          >
            Edit Racers
          </button>
          <button
            className={`px-4 py-2 rounded ${activeTab === "teams" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
            onClick={() => setActiveTab("teams")}
          >
            Edit Teams
          </button>
          <button
            className={`px-4 py-2 rounded ${activeTab === "entries" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
            onClick={() => setActiveTab("entries")}
          >
            Edit Entries
          </button>
        </div>

        <div className="bg-white p-4 border rounded shadow">{renderContent()}</div>
      </div>
    </PasswordGate>
  );
};

export default EditPanel;
