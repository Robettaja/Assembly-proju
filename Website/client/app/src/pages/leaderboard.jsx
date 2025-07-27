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
        setLeaderboard(data);
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
                                <th className="p-2">Fastest Lap</th>
    
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colSpan={6} className="h-4"></td>
                            </tr>
                            {leaderboard.length > 0 ? (
                                leaderboard.slice(0,10).map((user, index) => (
                                <tr key={index} class="border-b bg-gray-100 ">
                                    <td class="border-r p-4">{index + 1}</td>
                                    <td class="border-r">{user.user}</td>
                                    <td class="border-r p-2">{user.fastest_lap || '-'}</td>
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