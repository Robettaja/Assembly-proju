import React, {useState, useRef, useEffect} from "react";



const Countdown = () => {

    const [countdownTime, setCountdownTime] = useState(10);
    const [timerRunning, setTimerRunning] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);

    const countdownRef = useRef(null);
    const timerIntervalRef = useRef(null);
    const startTimeRef = useRef(null);

    const formatCountdown = (seconds) => {
        const m = String(Math.floor(seconds / 60)).padStart(2, "0");
        const s = String(seconds % 60).padStart(2, "0");
        return `${s}`;
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
   </div>
)};

export default Countdown;