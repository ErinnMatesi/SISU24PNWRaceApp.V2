import React, { useState } from "react";

const PasswordGate = ({ children }) => {
  const [input, setInput] = useState("");
  const [authorized, setAuthorized] = useState(false);

  const ADMIN_PASSWORD = process.env.REACT_APP_ADMIN_PASS;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input === ADMIN_PASSWORD) {
      setAuthorized(true);
    } else {
      alert("Incorrect password.");
    }
  };

  if (!authorized) {
    return (
      <form onSubmit={handleSubmit} className="p-6 max-w-md mx-auto">
        <h2 className="text-xl font-semibold mb-2">Admin Access</h2>
        <input
          type="password"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter admin password"
          className="w-full p-2 border rounded mb-4"
        />
        <button type="submit" className="bg-red-600 text-white px-4 py-2 rounded">
          Enter
        </button>
      </form>
    );
  }

  return <>{children}</>;
};

export default PasswordGate;
