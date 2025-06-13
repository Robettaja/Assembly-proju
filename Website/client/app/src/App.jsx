import { use, useEffect,useState, useRef} from 'react';
import './App.css'
import { VscChromeClose } from "react-icons/vsc";
import { VscArrowLeft } from "react-icons/vsc";
import Users from './pages/Users';
import Leaderboard from './pages/leaderboard';

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';



function App() {
  const [usernames, setUsernames] = useState([]);
  const [user, setUser] = useState("");
  const [email, setEmail] = useState("");
  const [username1, setUsername1] = useState("");
  const [username2, setUsername2] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [time, setTime] = useState('');
  const [laps1, setLaps1] = useState([]);
  const [laps2, setLaps2] = useState([]);
  const [userIds, setUserIds] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [laps, setLaps] = useState([]);
  const [elapsedTime, setElapsedTime] = useState(0);
  const intervalIdRef = useRef(null);
  const startTimeRef = useRef(0);
  const [lastUserId, setLastUserId] = useState(null);
  const [activeMenu, setActiveMenu] = useState(false);


  useEffect(() => {
    fetchUsernames();
  }, []);

  const fetchUsernames = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/usernames/");
      const data = await response.json();
      setUsernames(data);
    } catch (err) {
      console.log(err);
    }
  };

  const addUser = async (users) => {
    if (users.lenghth === 0) {
      console.warn("No users to add");
      return;
    }
    

    try {
      
      const response = await fetch("http://127.0.0.1:8000/api/usernames/create-multiple/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(users),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Backend error:", response.status, errorText);
        return;
      }

      const data = await response.json();
      setUsernames((prev) => [...prev, ...data]);
      console.log("Usernames added:", data);
      return data;

    } catch (err) {
      console.log("Fetch error:", err);
    }
    
  };

 

  const deleteUser = async (pk) => {
    try {
    
      const response = await fetch(`http://127.0.0.1:8000/api/usernames/${pk}/`, {
        method: "DELETE",
        });
      

      setUsernames((prev) => prev.filter((user) => user.id !== pk));
      }catch (err) {
        console.log(err);
        }  
    }



  const handleSubmit = async (e) => {
    e.preventDefault();

    const usersToAdd = [];
    if (username1.trim() !== "") usersToAdd.push({ user: username1 }); 
    if (username2.trim() !== "") usersToAdd.push({ user: username2 }); 

    const addedUsers = await addUser(usersToAdd);
    if (addedUsers) {
      setUserIds(addedUsers.map(u => u.id))
    }
    setSubmitted(true);
    const now = new Date();
    const formattedTime = now.toLocaleDateString();
    setTime(formattedTime);


   
  } 
  

      useEffect(() => {


        if(isRunning){
            intervalIdRef.current = setInterval(() => {
              setElapsedTime(Date.now() - startTimeRef.current);
            }, 10);

        }

        return () => {
          clearInterval(intervalIdRef.current);
        }
  
  
      }, [isRunning]);


      function start(){ 
          setIsRunning(true);
          startTimeRef.current = Date.now() - elapsedTime;
      } 
  
      const stop = async () => {
        setIsRunning(false);
        const lapTime = formatTime();
        setLaps((prev) => [...prev, lapTime]);

        if (lastUserId) {
          await fetch(`http://127.0.0.1:8000/api/usernames/${lastUserId}/`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json"},
            body: JSON.stringify({laptime: lapTime, user }),
          });
          fetchUsernames(); // Refresh the list of usernames
        }

        
      };
  
      function reset(){

        setElapsedTime(0);
        setIsRunning(false);  
        setLaps1([]);
        setLaps2([]);
      }
  
      function formatTime(){

        let hours = Math.floor(elapsedTime / (1000 * 60 * 60));
        let minutes = Math.floor(elapsedTime / (1000 * 60) % 60);
        let seconds = Math.floor(elapsedTime / (1000) % 60);
        let milliseconds = Math.floor(elapsedTime % 1000 / 10);
        
        hours = String(hours).padStart(2, "0");
        minutes = String(minutes).padStart(2, "0");
        seconds = String(seconds).padStart(2, "0");
        milliseconds = String(milliseconds).padStart(2, "0");
        return `${hours}:${minutes}:${seconds}:${milliseconds}`;
  
      }

      const handleLap1 = () => {
        if (laps1.length < 3) setLaps1([...laps1, formatTime()]);
      };

      const handleLap2 = () => {
        if (laps2.length < 3) setLaps2([...laps2, formatTime()]);
      };

      const totalTime = (laps) => {
        const toMs = (str) => {
          const [h, m, s, ms] = str.split(":").map(Number);
          return h * 3600000 + m * 60000 + s * 1000 + ms * 10;
        };

        const sum = laps.reduce((acc, lap) => acc + toMs(lap), 0);
        if (laps. length === 3) {
          let hours = Math.floor(sum / (1000 * 60 * 60));
          let minutes = Math.floor((sum / (1000 * 60)) % 60);
          let seconds = Math.floor((sum / 1000) % 60);
          let milliseconds = Math.floor((sum % 1000) / 10);
          hours = String(hours).padStart(2, "0");
          minutes = String(minutes).padStart(2, "0");
          seconds = String(seconds).padStart(2, "0");
          milliseconds = String(milliseconds).padStart(2, "0");
          return `${hours}:${minutes}:${seconds}:${milliseconds}`;
          }
          return "";
        };


  useEffect(() => {
    if (laps1.length === 3 && userIds[0]) {
      const total = totalTime(laps1);
      fetch(`http://127.0.0.1:8000/api/usernames/${userIds[0]}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ laptime: total }),
      }).then(fetchUsernames);
    }
  }, [laps1, userIds]);
  
  useEffect(() => {
    if (laps2.length === 3 && userIds[1]) {
      const total = totalTime(laps2);
      fetch(`http://127.0.0.1:8000/api/usernames/${userIds[1]}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ laptime: total }),
      }).then(fetchUsernames);
      }
  }, [laps2, userIds]);

  return (
    
<>






 
<div className = "App">
  <div className="video-background-container1">
        <video autoPlay muted loop playsInline className= "background-video blur-sm w-100">
          <source src="/videos/driftingcar.mp4" type= "video/mp4"/>
        </video>
  <Router>
    <div>
        <div className="nav-bar">
          <button
              onClick={() => {
                setActiveMenu(!activeMenu);
              }}
              className={`hamburger-menu ${activeMenu && "active"}`}
                  
              >
                  <span></span>
                  <span></span>
                  <span></span>
            </button>

            
            <div className={`${activeMenu ? "right-0" : "right-full"}
               h-screen w-full max-w-[400px] bg-zinc-800 absolute top-0 duration-500`}
              >
               <ul>
                      <li><Link to="/">Home</Link></li>
                      <li><Link to ="/users">Users</Link></li>
                      <li><Link to="/leaderboard">Leaderboard</Link></li>
              </ul>
            
            
              {activeMenu && (
                  <div className="menu">
                     

                  </div>
              )}
              </div>
        </div>
      <Routes>
        <Route path="/" element={

          
        <div>


      <div className="video-background-container">
        <video autoPlay muted loop playsInline className="background-video top-50px">
          <source src="/videos/driftingcar.mp4" type= "video/mp4"/>
        </video>


      <div className = "race">
      
          {!submitted ? (
            <div className="input-form">
              
              <form onSubmit = {handleSubmit}>
             
              <div className="flex flex-col md:flex-row gap-8 items-center justify-center w-full">
                <div className="input-container">
                  <label>
                    <p className="font-bold uppercase ">Player 1:</p>
                    <input
                      type ="text"
                      value={username1}
                      onChange={(e) => setUsername1(e.target.value)}
                      required
                    />
                  </label>
                </div>
                
                <div className="input-container">
                  <label>
                    <p className="font-bold uppercase ">Player 2:</p>
                    <input
                      type ="text"
                      value={username2}
                      onChange={(e) => setUsername2(e.target.value)}
                      required
                      />
                  </label>
                </div>
                </div>
                <div className="button-row">
                <button type="submit" className="w-300 h-300 bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-12 rounded-lg text-2xl uppercase tracking-wider transition-colors duration-300 transform hover:scale-105 shadow-lg">Start race</button>
                </div>
                <div className = "Hamk-logo-container">
                    <img src="/images/HAMK_Logo_horizontal_NEGA.png" alt="Hamk Logo"/>
                </div>
            </form>
            
          </div>
          
        ) : (
          
          <div className= "display-container">
            <div className="display">{formatTime()}</div>
            <h2>Race</h2>

              <button onClick={() => {
                setSubmitted(false)
                setUser("");
                reset();
              
              }} id="back-arrow">
                <VscArrowLeft />
              </button>
              <div className = "username-container">
                <div className="username-box">
                  <h2>{username1}</h2>
                  <div className="laps">
                    <p>lap1: {laps1[0] || ""}
                      <button className="button-lap" onClick={handleLap1} disabled = {laps1.length >= 3}>Lap</button>
                      </p> 
                    <p>lap2: {laps1[1] || ""}
                      <button className="button-lap" onClick={handleLap1} disabled = {laps1.length >= 3}>Lap</button>
                      </p> 
                    <p>lap3: {laps1[2] || ""}
                      <button className="button-lap" onClick={handleLap1} disabled = {laps1.length >= 3}>Lap</button>
                      </p> 
                    <p>Total: {totalTime(laps1)} 
                    </p>

                  </div>
                  <div>
                    <button onClick={start} className="start-button">Start</button>
                    <button onClick={stop} className="stop-button">Stop</button>
                  </div>
                </div>

                <div className="username-box">
                  <h2>{username2}</h2>
                  <div className="laps">
                    <p>lap1: {laps2[0] || ""}
                      <button className="button-lap" onClick={handleLap2} disabled = {laps2.length >= 3}>Lap</button>
                      </p> 
                    <p>lap2: {laps2[1] || ""}
                      <button className="button-lap" onClick={handleLap2} disabled = {laps2.length >= 3}>Lap</button>
                      </p> 
                    <p>lap3: {laps2[2] || ""}
                      <button className="button-lap" onClick={handleLap2} disabled = {laps2.length >= 3}>Lap</button>
                      </p> 
                    <p>Total: {totalTime(laps2)}
                    </p>


                  </div>

                    
                    <div>
                      <button onClick={start} className="start-button">Start</button>
                      <button onClick={stop} className="stop-button">Stop</button>
                    </div>
                  </div>
              </div>  
          </div>
        
        )}
      </div>
      </div>

 
        
      <div className="footer">
        <p>© 2023 Racetrack. All rights reserved.</p>
      </div>
    
    
        </div>


        } />
        <Route path="/users" element={
          <Users
            usernames = {usernames}
            deleteUser={deleteUser}
            />
        } />

        <Route path="/leaderboard" element={
          <Leaderboard usernames = {usernames} />
        } />

      </Routes>
          
  </div>

</Router>
</div>
</div>
</>
  );
}

export default App;