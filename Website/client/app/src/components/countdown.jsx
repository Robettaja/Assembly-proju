import React, { useState, useRef, useEffect } from "react";

const Countdown = ({ onLap, onFinish, userIds, username1, numLaps, onCountdownComplete }) => {
    const [countdownTime, setCountdownTime] = useState(2);
    const [timerRunning, setTimerRunning] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);

    const [user1Laps, setUser1Laps] = useState([]);
    const [user1Finished, setUser1Finished] = useState(false);

    const hasSavedRef = useRef(false);
    const countdownRef = useRef(null);
    const timerIntervalRef = useRef(null);
    const startTimeRef = useRef(null);
    const lapStartTimeRef = useRef(null);
    const user1FinishRef = useRef(null);

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
            triggerRaceStart(); // Lähettää käskyn API:lle
        }

        return () => clearInterval(countdownRef.current);
    }, [countdownTime]);

    useEffect(() => {
        if (timerRunning) {
            startTimeRef.current = Date.now();
            lapStartTimeRef.current = Date.now();
            timerIntervalRef.current = setInterval(() => {
                setElapsedTime(Date.now() - startTimeRef.current);
            }, 10);
        }

        return () => clearInterval(timerIntervalRef.current);
    }, [timerRunning]);

    useEffect(() => {
        if (user1Finished && !hasSavedRef.current) {
            hasSavedRef.current = true;
            clearInterval(timerIntervalRef.current);
            const user1Total = formatElapsed(user1FinishRef.current - startTimeRef.current);

            sendLapData({
                user_id: userIds[0],
                total_time: user1Total,
                laps: user1Laps.map((lap, i) => ({
                    lap_number: i + 1,
                    lap_time: lap,
                })),
            });

            onFinish?.({ user1Total });
        }
    }, [user1Finished]);

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

    const triggerRaceStart = async () => {
        try {
            console.log("Triggering race start via FLASK API");
            const response = await fetch("http://127.0.0.1:5000/start-race", {
                method: "POST",
            });
            if (!response.ok) throw new Error("Race start trigger failed");
            console.log("Flask acknowledged race start");
        } catch (err) {
            console.error("Failed to trigger race start:", err)
        }
    };

    const handleLap = () => {
        const now = Date.now();
        const lapDuration = now - lapStartTimeRef.current;
        lapStartTimeRef.current = now;
        const formattedLapTime = formatElapsed(lapDuration);

        setUser1Laps((prev) => {
            const updated = [...prev, formattedLapTime];
            console.log(`Lap ${updated.length}: ${formattedLapTime}`);
            onLap?.(0, formattedLapTime);

            if (updated.length === numLaps) {
                setUser1Finished(true);
                user1FinishRef.current = now;
                console.log("All laps completed");
            }

            return updated;
        });
    };

    return (
        <div className="p4 text-center">
            <h2 className="text-xl mb-2">Countdown</h2>
            <div className="text-4xl font-bold mb-4">
                {countdownTime > 0 ? countdownTime : formatElapsed(elapsedTime)}
            </div>

            {countdownTime === 0 && timerRunning && (
                <div className="flex justify-center gap-6">
                    <div>
                        <h3>{username1}</h3>
                        <button
                            onClick={handleLap}
                            disabled={user1Laps.length >= numLaps}
                            className="bg-blue-500 text-white px-4 py-2 rounded mb-2"
                        >
                            Lap
                        </button>
                        <h3>Laps:</h3>
                        <ul>
                            {user1Laps.map((lap, i) => (
                                <li key={i}>
                                    {i + 1}: {lap}
                                </li>
                            ))}
                        </ul>
                        {user1Laps.length === numLaps && (
                            <div>
                                <strong>Total time:</strong>{" "} 
                                {formatElapsed(user1FinishRef.current - startTimeRef.current)}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Countdown;
