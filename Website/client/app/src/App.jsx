import { useState } from 'react'
import './App.css'

function App() {
  const [usernames, setUsernames] = useState([]);

  useEffect(() => {
    fetchUsernames();
  }, []);

  const fetchUsernames = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/usernames/");
      const data = await response.json();
      console.log(data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <h1> Book website </h1>

      <div>
        <input type="text" placeholder="Input your username"/>
        <input type="text" placeholder="Input your email (optional)"/>
        <button> Add book </button>
      </div>
    </>
  )
}

export default App
