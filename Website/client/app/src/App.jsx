import { use, useEffect,useState, useRef} from 'react';
import './App.css'
import { VscChromeClose } from "react-icons/vsc";
import { VscArrowLeft } from "react-icons/vsc";
import Users from './pages/Users';
import Leaderboard from './pages/leaderboard';
import Countdown from './components/countdown'

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';



function App() {
  const [usernames, setUsernames] = useState([]);
  const [user, setUser] = useState("");
  const [email, setEmail] = useState("");
  const [username1, setUsername1] = useState("");
  const [username2, setUsername2] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [time, setTime] = useState('');

  const [userIds, setUserIds] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [laps, setLaps] = useState([[], []]);
  const [totalTimes, setTotalTimes] = useState({user1: "", user2: ""});

  const [elapsedTime, setElapsedTime] = useState(0);
  const intervalIdRef = useRef(null);
  const startTimeRef = useRef(0);

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
    if (users.length === 0) {
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
        return [];
      }

      const data = await response.json();
      setUsernames((prev) => [...prev, ...data]);
      return data;
    } catch (err) {
      console.log("Fetch error:", err);
      return [];
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
    if (addedUsers && addedUsers.length > 0) {
      setUserIds(addedUsers.map(u => u.id))
      setSubmitted(true);
      setUsername1(""); 
      setUsername2("");
      const now = new Date();
      const formattedTime = now.toLocaleDateString();
      setTime(formattedTime);
    } else
    {
      alert("Failed to add users. Please try again.");
    }
    
  };

  const handleLap = (userIndex, lapTime) => {
    const userId = userIds[userIndex];
    const currentLaps = laps[userIndex] || [];

    const lapIndex = currentLaps.length;
    saveLapTime(userId, lapIndex, lapTime);

    const updatedLaps = [...laps];
    updatedLaps[userIndex] = [...currentLaps, lapTime];
    setLaps(updatedLaps);
  };


  const handleFinish = (results) => {
    console.log("Race finished!");
    console.log("User 1 total time:", results.user1);
    console.log("User 2 total time:", results.user2);

    saveTotalTime(userIds[0], results.user1);
    saveTotalTime(userIds[1], results.user2);

    setTotalTimes(results);
  };

  

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



        
    const formatElapsed = (ms) => {
        const minutes = String(Math.floor(ms / 60000) % 60).padStart(2, "0");
        const seconds = String(Math.floor(ms / 1000) % 60).padStart(2, "0");
        const milliseconds = String(Math.floor((ms % 1000) / 10)).padStart(2, "0");
        return `${minutes}:${seconds}:${milliseconds}`;
    };
    


      
  return (

<div className = "App">
  <div className="video-background-container1">
        <video autoPlay muted loop playsInline className= "background-video-blur blur-sm w-100">
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
        </div>    
      <Routes>
          <Route path="/" element={

        <div>
          <div className="video-background-container">
            <video autoPlay muted loop playsInline className="background-video">
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
                          <button type="submit">
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                            Start race
                          </button>
                        </div>

                        <div className = "Hamk-logo-container">
                              <img src="/images/HAMK_Logo_horizontal_NEGA.png" alt="Hamk Logo"/>
                        </div>
                      </form>
                    
                    </div>
                  
                    ) : (
                  
                    <>
                        <div className= "display-container">
                          <Countdown
                            onFinish={handleFinish} onLap={(userIndex, lapTime) => handleLap(userIndex, lapTime)}/>

                            <div className="text-sm text-gray-700 text-center mt-2">
                                kierrokset: {laps[0].join(", ")} <br/>
                                Yhteensä: {totalTime.user1}
                            </div>

                            <div className="text-sm text-gray-700 text-center mt-2">
                                kierrokset: {laps[1].join(", ")} <br/>
                                Yhteensä: {totalTime.user2}
                            </div>

                        </div>
                        
                        

                        <button onClick={() => {
                          setSubmitted(false)
                          setUser("");
                          reset();
                        
                        }} id="back-arrow">
                          <VscArrowLeft />
                        </button>
                    </>
                )}
              </div>
                
          </div>  
          <div className="footer absolute bottom-0 left-0 w-full p-4 text-center text-gray-400 text-sm z-20">
                  <p>© 2025 Saija Joronen. All rights reserved.</p>
                </div>
        </div>
        }/>

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
            

    
    </Router>
  </div>
</div>
);
}

export default App;