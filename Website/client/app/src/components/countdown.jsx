import React, {useState, useRef, useEffect} from "react";



const Countdown = ({onLap, onFinish}) => {

    const [countdownTime, setCountdownTime] = useState(10);
    const [timerRunning, setTimerRunning] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);
    const [laps, setLaps] = useState([]);

    const countdownRef = useRef(null);
    const timerIntervalRef = useRef(null);
    const startTimeRef = useRef(null);

    const formatCountdown = (seconds) => {
        return String(seconds % 60).padStart(2, "0");
    };

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
        }

        return () => clearInterval(countdownRef.current);
     }, [countdownTime]);

     useEffect(() => {
        if(timerRunning) {
           startTimeRef.current = Date.now();
            timerIntervalRef.current = setInterval(() => {
                setElapsedTime(Date.now() - startTimeRef.current);
            }, 10);
        }
            return () => clearInterval(timerIntervalRef.current)
            
     }, [timerRunning]);

     const handleLap = () => {
        const lapTime = formatElapsed(elapsedTime);
        const updatedLaps = [...laps, lapTime];
        setLaps(updatedLaps);

        if (onLap) onLap(lapTime);

        if (updatedLaps.length === 3) {
            clearInterval(timerIntervalRef.current);
            setTimerRunning(false);

            const total = totalTime(updatedLaps);
            if (onFinish) onFinish(total);
        }
    };

        const totalTime = (laps) => {
            const toMs = (str) => {
                const [m, s, ms] = str.split(":").map(Number);
                return m * 60000 + s * 1000 + ms * 10;
            };
            const sum = laps.reduce((acc, lap) => acc + toMs(lap), 0);
            const minutes = String(Math.floor(sum / 60000) % 60).padStart(2, "0");
            const seconds = String(Math.floor(sum / 1000) % 60).padStart(2, "0");
            const milliseconds = String(Math.floor((sum % 1000) / 10)).padStart(2, "0");
            return `${minutes}:${seconds}:${milliseconds}`;
        };

    const saveLapTime = (userId, lapIndex, time) => {
        const field = `lap${lapIndex + 1}`;
          return fetch(`http://127.0.0.1:8000/api/usernames/${userId}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                [field]: time,
            }),
          });
    };

    const saveTotalTime = (userId, total) => {
          return fetch(`http://127.0.0.1:8000/api/usernames/${userId}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                total_time: total,
            }),
          });
        };
    


   


    return (
    <div className="">
    
        <h2>Countdown</h2>
        <div className="w-100 flex flex-row justify-center mx-auto">
             <div className="countdown-box">
                <div className="countdown-value">
                    {!timerRunning ? (
                        <h2>{formatCountdown(countdownTime)}</h2>
                    ) : (
                        <h2>{formatElapsed(elapsedTime)}</h2>
                    )}
                    
                </div>
            </div>   
        </div>

        {timerRunning && (
            <div className = "flex flex-col items-center mt-4 gap-2">
                <button onClick = {handleLap} className="button-lap">
                laptime
                </button>
                </div>
        )}
    </div>
    );
};

export default Countdown;