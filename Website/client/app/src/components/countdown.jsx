import React, { useState, useRef, useEffect } from "react";

const Countdown = ({ onLap, onFinish, userIds, username1, username2, numLaps, onCountdownComplete }) => {
    const [countdownTime, setCountdownTime] = useState(10);
    const [timerRunning, setTimerRunning] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);

    const [user1Laps, setUser1Laps] = useState([]);
    const [user2Laps, setUser2Laps] = useState([]);

    const [user1Finished, setUser1Finished] = useState(false);
    const [user2Finished, setUser2Finished] = useState(false);

    const countdownRef = useRef(null);
    const timerIntervalRef = useRef(null);
    const startTimeRef = useRef(null);
    const lapStartTimeRefs = useRef([null, null]);

    const user1FinishRef = useRef(null);
    const user2FinishRef = useRef(null);

    const formatElapsed = (ms) => {
        const minutes = String(Math.floor(ms / 60000) % 60).padStart(2, "0");
        const seconds = String(Math.floor(ms / 1000) % 60).padStart(2, "0");
        const milliseconds = String(Math.floor((ms % 1000) / 10)).padStart(2, "0");
        return `${minutes}:${seconds}:${milliseconds}`;
    };

    useEffect(() => {
        if (countdownTime > 0) {
            countdownRef.current = setInterval(() => {
                setCountdownTime((prev) => prev - 1);
            }, 1000);
        }

        if (countdownTime === 0) {
            clearInterval(countdownRef.current);
            setTimerRunning(true);
            onCountdownComplete?.(); // Laukaise auton liikkeelle
        }

        return () => clearInterval(countdownRef.current);
    }, [countdownTime]);

    useEffect(() => {
        if (timerRunning) {
            startTimeRef.current = Date.now();
            lapStartTimeRefs.current = [Date.now(), Date.now()];
            timerIntervalRef.current = setInterval(() => {
                setElapsedTime(Date.now() - startTimeRef.current);
            }, 10);
        }

        return () => clearInterval(timerIntervalRef.current);
    }, [timerRunning]);

    useEffect(() => {
        if (user1Finished && user2Finished) {
            clearInterval(timerIntervalRef.current);
            const user1Total = formatElapsed(user1FinishRef.current - startTimeRef.current);
            const user2Total = formatElapsed(user2FinishRef.current - startTimeRef.current);
            sendLapData([
                {
                    user_id: userIds[0],
                    total_time: user1Total,
                    laps: user1Laps.map((lap, i) => ({ lap_number: i + 1, lap_time: lap })),
                },
                {
                    user_id: userIds[1],
                    total_time: user2Total,
                    laps: user2Laps.map((lap, i) => ({ lap_number: i + 1, lap_time: lap })),
                },
            ]);
            onFinish && onFinish({ user1: user1Total, user2: user2Total });
        }
    }, [user1Finished, user2Finished]);

    const sendLapData = async (data) => {
        try {
            console.log("Sending lap data:", data);
            const response = await fetch("http://127.0.0.1:8000/api/save-laps/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            if (!response.ok) throw new Error("Lap data save failed");
            const resData = await response.json();
            console.log("Lap data saved:", resData);
        } catch (err) {
            console.error("Error sending lap data:", err);
        }
    };

    const handleLap = (userIndex) => {
        const now = Date.now();
        const lapDuration = now - lapStartTimeRefs.current[userIndex];
        lapStartTimeRefs.current[userIndex] = now;
        const formattedLapTime = formatElapsed(lapDuration);

        if (userIndex === 0) {
            setUser1Laps((prev) => {
                const updated = [...prev, formattedLapTime];
                onLap && onLap(0, formattedLapTime);



                if (updated.length === numLaps) {
                    setUser1Finished(true);
                    user1FinishRef.current = now;
                }
                return updated;
            });
        }

        if (userIndex === 1) {
            setUser2Laps((prev) => {
                const updated = [...prev, formattedLapTime];
                onLap && onLap(1, formattedLapTime);


                if (updated.length === numLaps) {
                    setUser2Finished(true);
                    user2FinishRef.current = now;
                }
                return updated;
            });
    
        }
    };
    

    return (
        <div className="p4 text-center">
            <h2 className="text-x1 mb-2">Countdown / timer</h2>
            <div className="text-4x1 font-bold mb-4">
                {countdownTime > 0 ? countdownTime : formatElapsed(elapsedTime)}
            </div>

            {countdownTime === 0 && timerRunning && (
                <div className="flex justify-center gap-6">
                    {/* User 1 */}
                    <div>
                        <h3>{username1}</h3>
                        <button
                            onClick={() => handleLap(0)}
                            disabled={user1Laps.length >= numLaps}
                            className="bg-blue-500 text-white px-4 py-2 rounded mb-2"
                        >
                            Lap
                        </button>
                        <h3>Laps:</h3>
                        <ul>{user1Laps.map((lap, i) => <li key={i}>{lap}</li>)}</ul>
                        {user1Laps.length === numLaps && (
                            <div>
                                Total time: {formatElapsed(user1FinishRef.current - startTimeRef.current)}
                            </div>
                        )}
                    </div>

                    {/* User 2 */}
                    <div>
                        <h3>{username2}</h3>
                        <button
                            onClick={() => handleLap(1)}
                            disabled={user2Laps.length >= numLaps}
                            className="bg-green-500 text-white px-4 py-2 rounded mb-2"
                        >
                            Lap
                        </button>
                        <h3>Laps:</h3>
                        <ul>{user2Laps.map((lap, i) => <li key={i}>{lap}</li>)}</ul>
                        {user2Laps.length === numLaps && (
                            <div>
                                Total time: {formatElapsed(user2FinishRef.current - startTimeRef.current)}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Countdown;