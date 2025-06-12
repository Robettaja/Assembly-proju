import React, { useState } from 'react';

const Leaderboard = ({usernames}) => {
    const sorted = usernames
        .filter(u => u.laptime)
        .sort((a, b) => a.laptime.localeCompare(b.laptime));
        

    const topUser = sorted[0]

    return (
        <div className="leaderboard">
            <h1>Leaderboard</h1>
            <table className="leaderboard-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Username</th>
                        <th>Total time</th>
                        <th>Lap 1</th>
                        <th>Lap 2</th>
                        <th>Lap 3</th>
                    </tr>
                </thead>
                <tbody>
                    {sorted.length > 0 ? (
                        sorted.map((user, index) => (
                        <tr key={user.id}>
                            <td>{index + 1}</td>
                            <td>{user.user}</td>
                            <td>{user.laptime}</td>
                            <td>{user.lap1 || '-'}</td>
                            <td>{user.lap2 || '-'}</td>
                            <td>{user.lap3 || '-'}</td>
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
    );
};


export default Leaderboard;