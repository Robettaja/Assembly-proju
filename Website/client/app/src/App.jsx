import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1> Book website </h1>

      <div>
        <input type="text" placeholder="Book title..."></input>
        <input type="number" placeholder="Release date"></input>
        <button>Add book </button>
      </div>
    </>
  )
}

export default App
