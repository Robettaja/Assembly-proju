import { use, useEffect,useState } from 'react'
import './App.css'

function App() {
  const [usernames, setUsernames] = useState([]);
  const [user, setUser] = useState("");
  const [email, setEmail] = useState("");

  const [newTitle, setNewTitle] = useState("");

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
      user: newTitle,
      email: email,
    };

    try {
    
      const response = await fetch(`http://127.0.0.1:8000/api/usernames/${pk}`, {
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
      
    }
     catch (err) {
        console.log(err);
      }
  } 

  const deleteUser = async (pk) => {
    try {
    
      const response = await fetch(`http://127.0.0.1:8000/api/usernames/${pk}`, {
        method: "DELETE",
        });
      

      setUsernames((prev) => prev.filter((user) => user.id !== pk));
      }catch (err) {
        console.log(err);
        }  
}


return (
    <>
      <h1> Auto kilpailu </h1>

      <div>
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
        <input type ="text" placeholder="New title..." />
        <button onClick={ () => updateTitle(username.id, username.email)}>Change</button>
        <button onClick={() => deleteUser(username.id)}> DELETE </button>
        </div>
      )}
          </>
  )
}

export default App
