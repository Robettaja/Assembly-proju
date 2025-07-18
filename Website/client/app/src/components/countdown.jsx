import React, {useState, useRef, useEffect} from "react";



const Countdown = ({onLap, onFinish}) => {

    const [countdownTime, setCountdownTime] = useState(10);
    const [timerRunning, setTimerRunning] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);

    const [user1Laps, setUser1Laps] = useState([]);
    const [user2Laps, setUser2Laps] = useState([]);
    
    const countdownRef = useRef(null);
    const timerIntervalRef = useRef(null);
    const startTimeRef = useRef(null);
    const lapStartTimeRef = useRef(null);

    const user1FinishRef = useRef(null);
    const user2FinishRef = userRef(null);

    const formatElapsed = (ms) => {
        const minutes = String(Math.floor(ms / 60000) % 60).padStart(2, "0");
        const seconds = String(Math.floor(ms / 1000) % 60).padStart(2, "0");
        const milliseconds = String(Math.floor((ms % 1000) / 10)).padStart(2, "0");
        return `${minutes}:${seconds}:${milliseconds}`;
    };

    const totalTime = (lapsArray) => {
        let totalMs = 0;
        lapsArray.forEach(time => {
            const [min, sec, ms] = time.split(':').map(Number);
            totalMs += min * 60000 + sec * 1000 + ms * 10;
        });
        return formatElapsed(totalMs);
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
            lapStartTimeRef.current = Date.now();
            timerIntervalRef.current = setInterval(() => {
                setElapsedTime(Date.now() - startTimeRef.current);
            }, 10);
        }
            return () => clearInterval(timerIntervalRef.current)
            
     }, [timerRunning]);

    const handleLap = (userIndex) => {
        const now = Date.now();
        const lapDuration = now - lapStartTimeRef.current;
        lapStartTimeRef.current = now;

        const formattedLapTime = formatElapsed(lapDuration);

        if (userIndex === 0 && user1Laps.length < 3) {
            const updated = [...user1Laps, formattedLapTime];
            setUser1Laps(updated);
            onLap && onLap(0, formattedLapTime);

            if (updated.length === 3) {
                user1FinishRef.current.now;
            }

            if (user2Laps === 3 && updated.length === 3 && onFinish) {
                clearInterval(timerIntervalRef.current);

                const user1Total = formatElapsed(user1FinishRef.current - startTimeRef.current);
                const user2Total = formatElapsed(user2FinishRef.current - startTimeRef.current);

                onFinish({
                    user1: user1Total,
                    user2: user2Total
                });

            }
            return;
        }
        

        if (userIndex === 1 && user2Laps.length < 3) {
            const updated = [...user2Laps, formattedLapTime];
            setUser2Laps(updated);
            onLap && onLap(1, formattedLapTime);
            
           if (updated.length === 3) {
            user2FinishRef.current = now;
            }

            if (user1Laps.length === 3 && updated.length === 3 && onFinish) {
                clearInterval(timerIntervalRef.current);

                const user1Total = formatElapsed(user1FinishRef.current - startTimeRef.current);
                const user2Total = formatElapsed(user2FinishRef.current - startTimeRef.current);

                onFinish({
                    user1: user1Total,
                    user2: user2Total
                })
            }
        
        }



        return;
    };
        

 

    



   


    return (
        <div className="p4 text-center">
        
            <h2 className="text-x1 mb-2">Countdown / Timer</h2>
            <div className="text-4x1 font-bold mb-4">
                {countdownTime > 0 ? countdownTime : formatElapsed(elapsedTime)}
            </div>

            {countdownTime === 0 && timerRunning && (
                <div className="flex justify-center gap-6">
                    <div>
                        <h3 className="text-x1 mb-2"> User 1</h3>
                
                        <button
                            onClick={() => handleLap(0)}
                            disabled={user1Laps.length >= 3}
                            className="bg-blue-500 text-white px-4 py-2 rounded mb-2"
                            >
                            Lap
                        </button>
                    
                        <h3>Laps:</h3>
                        <ul>
                            {user1Laps.map((lap, i) => (
                                <li key = {i}>{lap}</li>
                            ))}
                        </ul>
                    
                    </div>

                    <div>
                        <h3 className="text-x1 mb-2"> User 2</h3>
                        <button 
                            onClick={() => handleLap(1)}
                            disabled={user2Laps.length >= 3}
                            className="bg-green-500 text-white px-4 py-2 rounded mb-2"
                            >
                            Lap
                        </button>

                        <h3>Laps: </h3>
                        <ul>
                            {user2Laps.map((lap, i) => (
                                <li key = {i}> {lap} </li>
                        ))}    
                        </ul>    

                        
                    </div>
                </div>
            )}

           
        </div>
        );
    };

export default Countdown;