import { use, useEffect,useState, useRef} from 'react';
import './App.css'
import { VscChromeClose } from "react-icons/vsc";
import { VscArrowLeft } from "react-icons/vsc";
import Users from './pages/Users';

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';



function App() {
  const [usernames, setUsernames] = useState([]);
  const [user, setUser] = useState("");
  const [email, setEmail] = useState("");
  const [username1, setUsername1] = useState("");
  const [username2, setUsername2] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [time, setTime] = useState('');

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
    
    await addUser(usersToAdd);
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

        reset();
      };
  
      function reset(){

        setElapsedTime(0);
        setIsRunning(false);  
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

  return (
    
<>



      {/*

```
      <h1> Auto kilpailu </h1>
      <div class = "input-container">
        <input type="text" placeholder="Input your username" 
        onChange = {(e) => setUser(e.target.value)}
        />
        <input type="text" placeholder="Input your email (optional)"
        onChange = {(e) => setEmail(e.target.value)}
        />
        <button onClick = {addUser}> Submit </button>
      </div>
      {usernames.map((username) => 
      <div> 
        <p>Username: {username.user} </p> 
        <p>Email: {username.email} </p>  
        <input type ="text" placeholder="New title..." value={newTitle[username.id] || ""}
        onChange = {(e) => 
          setNewTitle((prev) => ( {
            ...prev, [username.id]: e.target.value
          }))
         }
        />
        <button onClick={ () => updateTitle(username.id, username.email)}>Change</button>
        <button onClick={() => deleteUser(username.id)}> DELETE </button>
        </div>
      )}



*/}    
  <Router>
    <div>
        <div className="nav-bar">
            
            <div className={`${activeMenu ? "right-0" : "right-[400px]"}
              } h-screen w-full max-w-[400px] bg-zinc-800 absolute top-0 duration-500`}
              >
              <ul>
                      <li><Link to="/">Home</Link></li>
                      <li><Link to ="/users">Users</Link></li>
              </ul>

            <button
              onClick={() => {
                setActiveMenu(!activeMenu);
              }}
              className={`hamburger-menu ${activeMenu && "active"}`}
                  
              >
                  <span className="bar"></span>
                  <span className="bar"></span>
                  <span className="bar"></span>
            </button>

            
              {activeMenu && (
                  <div className="menu">
                    
                  </div>
              )}
              </div>
        </div>
      <Routes>
        <Route path="/" element={

          
        <div>



      <div>
        <h1>Racetrack</h1>
        <p>Enter your username and email to race</p>
      </div>

      <div className = "input-form">
        {!submitted ? (
          <form onSubmit = {handleSubmit}>
            <h2>Input usernames</h2>
            <div className="input-container">
              <label>
                Player 1:
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
                Player 2:
                <input
                  type ="text"
                  value={username2}
                  onChange={(e) => setUsername2(e.target.value)}
                  required
                  />
              </label>
            </div>

            <button type="submit">Start race</button>
          </form>

        ) : (
          
          <div className= "display-container">
            <div className="display">{formatTime()}</div>
            <h2>Race</h2>

              <button onClick={() => {
                setSubmitted(false)
                setUser("");
              
              }} id="back-arrow">
                <VscArrowLeft />
              </button>

            <div className="username-box">
              <p>{username1}</p>
              <div>
                <button onClick={start} className="start-button">Start</button>
                <button onClick={stop} className="stop-button">Stop</button>
              </div>
            </div>

           <div className="username-box">
              <p>{username2}</p>
              <div>
                <button onClick={start} className="start-button">Start</button>
                <button onClick={stop} className="stop-button">Stop</button>
              </div>
            </div>

          </div>
        
        )}
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

      </Routes>
          
  </div>

</Router>

</>
  );
}

export default App;