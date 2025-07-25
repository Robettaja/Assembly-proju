import React, { useState, useEffect } from 'react';
import {VscChromeClose} from 'react-icons/vsc';
import TextField from '@mui/material/TextField';
import Pagination from '../components/pagination'




const Users = ({usernames, deleteUser}) => {

    const [search, setSearch] = useState("");
    const [names, setNames] = useState([]);

    const [currentPage, setCurrentPage] = useState(1);
    const [namesPerPage] = useState(10);

 


    const filteredUsers = usernames.filter((username) =>
        username.user.toLowerCase().includes(search.toLowerCase()) ||
        (username.email && username.email.toLowerCase().includes(search.toLowerCase()))
    );

    const indexOfLastNames = currentPage * namesPerPage;
    const indexOfFirstNames = indexOfLastNames - namesPerPage;
    const currentUsers = filteredUsers.slice(indexOfFirstNames, indexOfLastNames);


    useEffect (() => {
        const fetchNames = async () => {
            const res = await fetch("http://127.0.0.1:8000/api/usernames/");
            const data = await res.json();
            setNames(data);
        };

        fetchNames();
    }, []);

    return (
        <>
            <div className='heading'>
                <h1>Users</h1>
                
                <Pagination
                    namesPerPage={namesPerPage}
                    totalNames={filteredUsers.length}
                    setCurrentPage={setCurrentPage}
                    currentPage={currentPage}
                    />
            </div>

            <div className = "searchbar">
                <h1>Search</h1>
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

            <div className='max-h-[700vh]'>
                <h2>Users</h2>
                {currentUsers.map((username) => (
                    <div className="saved-data" key={username.id}>
                        <button onClick={() => deleteUser(username.id)} id="x-button">
                            <VscChromeClose />
                        </button>

                        <div className="username-email">
                            Username: {username.user} <br />
                            
                            Laptime: {username.total_time}
                        </div>
                    </div>
                ))}
           </div>  
        </>
    );

}


export default Users;