import React, { useState, useEffect } from 'react';
import {VscChromeClose} from 'react-icons/vsc';
import TextField from '@mui/material/TextField';
import Pagination from '../components/pagination'




const Users = ({deleteUser}) => {

    const [search, setSearch] = useState("");
    const [users, setUsers] = useState([]);

    const [currentPage, setCurrentPage] = useState(1);
    const [namesPerPage] = useState(10);

     useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                const res = await fetch("http://127.0.0.1:8000/api/leaderboard/");
                const data = await res.json();
                setUsers(data);
            } catch (error) {
                console.error("Failed to fetch leaderboard:", error);
            }
        };
        fetchLeaderboard();
    }, []);
  


    const filteredUsers = users.filter((user) =>
        user.user.toLowerCase().includes(search.toLowerCase())
        
    );

    const indexOfLastNames = currentPage * namesPerPage;
    const indexOfFirstNames = indexOfLastNames - namesPerPage;
    const currentUsers = filteredUsers.slice(indexOfFirstNames, indexOfLastNames);


    // useEffect (() => {
    //     const fetchNames = async () => {
    //         const res = await fetch("http://127.0.0.1:8000/api/usernames/");
    //         const data = await res.json();
    //         setNames(data);
    //     };

    //     fetchNames();
    // }, []);



    return (
        <>
          <div className='flex flex-col pt-2 px-6 h-full'>
             
            <div className='flex flex-col gap-6 p-6 max-w-4xl mx-auto my-8'>
                <h1 className='text-3x1 font-bold text-center text-gray-800'>Users</h1>
                    <div className='mt-4 flex justify-center'>
                        <Pagination
                            namesPerPage={namesPerPage}
                            totalNames={filteredUsers.length}
                            setCurrentPage={setCurrentPage}
                            currentPage={currentPage}
                            />  
                    </div>
            </div>

            <div className = "flex flex-col gap-2">
                <h1 className='text-x1 font-semibold text-gray-700'>Search</h1>
                <div className="search-container">
                    <TextField
                        id="outlined-basic"
                        variant="outlined"
                        fullWidth
                        label="Search"
                        value={search}
                        onChange={(e) => {
                            setSearch(e.target.value)
                            setCurrentPage(1);
                        }}
                    />

                </div> 
            </div>

            <div className='flex flex-col gap-4'>
                
                {currentUsers.map((user) => (
                    <div className="flex justify-between items-center border border-gray-300 rounded-lg p-4 shadow-ms hover:shadow-md transition"
                     key={user.user}>

                        <button onClick={() => deleteUser(user.id)} 
                            className="text-red-500 hover:text-red-700"
                            aria-label="Delete">
                            <VscChromeClose size={20} />
                        </button>

                        <div className="username-email">
                            <p className='text-lg font-medium'>Username: {user.user}</p> <br />
                            
                            <p className='text-sm text-gray-600'>Fastest lap time: {user.fastest_lap}</p>
                        </div>
                    </div>
                ))}
           </div>  
        
          </div>
        </>
    );

}


export default Users;