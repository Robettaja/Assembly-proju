import React, { useState } from 'react';
import {VscChromeClose} from 'react-icons/vsc';
import TextField from '@mui/material/TextField';


const Users = ({usernames, deleteUser}) => {

    const [search, setSearch] = useState("");

    const filteredUsers = usernames.filter((username) =>
        username.user.toLowerCase().includes(search.toLowerCase()) ||
        (username.email && username.email.toLowerCase().includes(search.toLowerCase()))
    );



    return (
        <>
    <div className = "searchbar">
        <h1>Search</h1>
        <div className="search-container">
            <TextField
                id="outlined-basic"
                variant="outlined"
                fullWidth
                label="Search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                />

        </div>

        
    </div>
    <div>
        <h2>Users</h2>
        {filteredUsers.map((username) => (
            <div className="saved-data" key={username.id}>
                <button onClick={() => deleteUser(username.id)} id="x-button">
                    <VscChromeClose />
                </button>

            <div className="username-email">
                Username: {username.user} <br />
                Email: {username.email} <br />
                Laptime: {username.lapTime}
            </div>
        </div>
       ))}
    </div>
      
    </>
    );

}


export default Users;