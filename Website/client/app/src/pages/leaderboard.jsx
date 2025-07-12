import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
    const [leaderboard, setLeaderboard] = useState([]);

    useEffect(() => { 
        fetchLeaderboard();

}, []);

const fetchLeaderboard = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/usernames/");
        const data = await response.json();

        const sorted = data
            .filter(user => user.total_time)
            .sort((a, b) => {
                const timeToMs = (time) => {
                    const [m, s, ms] = time.split(":").map(Number);
                    return m * 60000 + s * 1000 + ms * 10;
                };
                return timeToMs(a.total_time) - timeToMs(b.total_time); 
            });

    setLeaderboard(sorted);
    } catch (err) {
        console.error("Leaderboard error:", err);
    }
};
    return (
        <div className="App">
            <div className="p-4">
                <h1 className="m-6 text-white text-2x1">Leaderboard</h1>
                <div className="max-h-[700vh] border rounded sh">    
                    <table className="min-w-full ">
                        <thead className="bg-gray-200 sticky top-0">
                            <tr className="shadow-md my-8">
                                <th className="p-2">#</th>
                                <th className="p-2">Username</th>
                                <th className="p-2">Total time</th>
                                <th className="p-2">Lap 1</th>
                                <th className="p-2">Lap 2</th>
                                <th className="p-2">Lap 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colSpan={6} className="h-4"></td>
                            </tr>
                            {leaderboard.length > 0 ? (
                                leaderboard.slice(0,10).map((user, index) => (
                                <tr key={user.id} class="border-b bg-gray-100 ">
                                    <td class="border-r p-4">{index + 1}</td>
                                    <td class="border-r">{user.user}</td>
                                    <td class="border-r p-2">{user.total_time}</td>
                                    <td class="border-r p-2">{user.lap1 || '-'}</td>
                                    <td class="border-r p-2">{user.lap2 || '-'}</td>
                                    <td class=" p-2">{user.lap3 || '-'}</td>
                                </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6">No data available</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};


export default Leaderboard;