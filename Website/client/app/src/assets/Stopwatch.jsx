import React, {useStte, useEffect, useRef} from 'react';

function Stopwatch () {


    const [isRunning, setIsRunning] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);
    const intervalIdRef = useRef(null);
    const startTimeRef = useRef(0);

    useEffect(() => {


    }, [isRunning]);
    function start(){

    }

    function stop(){

    }

    function reset(){

    }

    function formatTime(){

        return `00:00:00`;

    }


    return(
    
    <>
    
    <div className = "stopwatch">
        <div className = "display">{formatTime()}</div>
        <div className = "controls">
            <button onClick = {start} classname = "start-button">Statt</button>
            <button onClick = {stop} classname = "stop-button">stop</button>
            <button onClick = {reset} classname = "reset-button">reset</button>



        </div>



        </div>
        
        
        </>)

    }

export default Stopwatch