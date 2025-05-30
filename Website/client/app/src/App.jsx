import { use, useEffect,useState, useRef} from 'react';
import './App.css'

function App() {
  const [usernames, setUsernames] = useState([]);
  const [user, setUser] = useState("");
  const [email, setEmail] = useState("");
  const [newTitle, setNewTitle] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [time, setTime] = useState('');

  const [isRunning, setIsRunning] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const intervalIdRef = useRef(null);
  const startTimeRef = useRef(0);


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

  const addUser = async () => {
    const userData = {
      user: user,
      email: email,
    };

    try {
    
      const response = await fetch("http://127.0.0.1:8000/api/usernames/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),

      });
      const data = await response.json();
      setUsernames((prev) => [...prev, data]);
      console.log(data);
    }
     catch (err) {
        console.log(err);
      }
    
  };

  const updateTitle = async (pk, email) => {
     const userData = {
      user: newTitle[pk],
      email: email,
    };

    try {
    
      const response = await fetch(`http://127.0.0.1:8000/api/usernames/${pk}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),

      });
      const data = await response.json();
      setUsernames((prev) => 
        prev.map((user) => {
          if (user.id === pk)
          {
            return data;
          }
          else {
            return user;
          }}
          )
      );

      setNewTitle((prev) => {
        const updated = {...prev};
        delete updated[pk];
        return updated;
      });
    }
     catch (err) {
        console.log(err);
      }
  } 

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

{/* username input and timer */}

  const handleSubmit = (e) => {
    e.preventDefault();
    addUser();
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
  
      function stop(){
        setIsRunning(false);


      }
  
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
  <div>
  <h1>Racetrack</h1>
  <p>Enter you username and email to race</p>
  </div>


    <div class =  "input-container">
      {!submitted ? (
      <>
        <form onSubmit = {handleSubmit}>
            <label>
              Username:
              <input
                type = "text" 
                value = {user}
                onChange = {(e) => setUser(e.target.value)}
                required
              />
            </label>
            <label>
              Email:
              <input
              type = "text"
              value = {email}
              onChange = {(e) => setEmail(e.target.value)}
              
              />
            </label>

            
            <button onClick = {addUser} type="submit"> Lähetä </button>
          </form>
    

          </>     
        ) : (
          <>
      <div>
        <h1>Hei, {user}!</h1>
        <p>Nykyinen aika on:  </p>
        <div className = "stopwatch">
          <div className = "display">{formatTime()}</div>
          <div className = "controls">
              <button onClick = {start} className = "start-button">Statt</button>
              <button onClick = {stop} className = "stop-button">stop</button>
              <button onClick = {reset} className = "reset-button">reset</button>
            </div>
    
    </div>
          <button onClick={() => setSubmitted(false)}>Palaa takaisin</button>
        

        
      </div>

    
    </>
    )}
  

    </div>
    {usernames.map((username) => (
          <div class = "saved-data" key = {username.id}> 
            <p> Username: {username.user} </p> 
            <p>Email: {username.email} </p>  
            <button onClick={() => deleteUser(username.id)}> DELETE </button>
            </div>
          ))}
 </>
  );
  
  }


export default App
