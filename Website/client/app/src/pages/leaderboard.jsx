import React, { useState } from 'react';

const Leaderboard = ({usernames}) => {
    const sorted = usernames
        .filter(u => u.laptime)
        .sort((a, b) => a.laptime.localeCompare(b.laptime));
        

    const topUser = sorted[0]

    return (
        <div className="App">
        <div className="p-4">
            <h1 class="m-6 text-white text 2x1">Leaderboard</h1>
            <div className="overflow-auto max-h-[700vh] border rounded sh">    
            <table class="min-w-full ">
                <thead class="bg-gray-200 sticky top-0 z-10">
                    <tr class="shadow-md my-8">
                        <th class="p-2">#</th>
                        <th class="p-2">Username</th>
                        <th class="p-2">Total time</th>
                        <th class="p-2">Lap 1</th>
                        <th class="p-2">Lap 2</th>
                        <th class="p-2">Lap 3</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td colSpan={6} className="h-4"></td>
                    </tr>
                    {sorted.length > 0 ? (
                        sorted.slice(0,10).map((user, index) => (
                        <tr key={user.id} class="border-b bg-gray-100 ">
                            <td class="border-r p-4">{index + 1}</td>
                            <td class="border-r">{user.user}</td>
                            <td class="border-r p-2">{user.laptime}</td>
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