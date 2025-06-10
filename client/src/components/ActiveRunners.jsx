// import React, { useState, useEffect } from "react";
// import axios from "axios";

// export default function ActiveRunners() {
//     const [activeRunners, setActiveRunners] = useState([]);

//     useEffect(() => {
//         fetchActiveRunners();
//     }, []);

//     const fetchActiveRunners = async () => {
//         try {
//             const response = await axios.get("/active-runners");
//             setActiveRunners(response.data);
//         } catch (error) {
//             console.error(error);
//         }
//     };

//     return (
//         <div className="active-runners-container">
//             <h2>Active Runners</h2>
//             <ul>
//                 {activeRunners.map((runner) => (
//                     <li key={runner.racer_id}>
//                         {runner.first_name} {runner.last_name} - Started: {new Date(runner.start_time).toLocaleString()}
//                     </li>
//                 ))}
//             </ul>
//         </div>
//     );
// }
