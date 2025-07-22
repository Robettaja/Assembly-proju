import React, { useState, useEffect } from 'react';
import {VscChromeClose} from 'react-icons/vsc';
import TextField from '@mui/material/TextField';



const Users = ({usernames, deleteUser}) => {

    const [search, setSearch] = useState("");
    const [names, setNames] = useState([]);

    const [currentPage, setCurrentPage] = useState(1);
    const [namesPerPage] = useState(10);

    const indexOfLastNames = currentPage * namesPerPage;
    const indexOfFirstNames = indexOfLastNames * namesPerPage;
    const currentNames = names.slice(indexOfFirstNames, indexOfLastNames);



    const filteredUsers = usernames.filter((username) =>
        username.user.toLowerCase().includes(search.toLowerCase()) ||
        (username.email && username.email.toLowerCase().includes(search.toLowerCase()))
    );

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
        <NamesList names={names}/>
        <Pagination
            namesPerPage={namesPerPage}
            totalNames={names.length}
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
                onChange={(e) => setSearch(e.target.value)}
                />

        </div>

        
    </div>
    <div className='max-h-[700vh]'>
        <h2>Users</h2>
        {filteredUsers.map((username) => (
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

const NamesList = ({ names }) => {
    return (
        <ul className='list-group'>
            {names.map((names) => (
                <li key={names.id} className='list-group-item'>
                    <h3>username: {names.user}</h3>
                    <h3>Total time: {names.total_time}</h3>
                </li>
            ))}
        </ul>
    );
};

const Pagination = ({
    namesPerPage,
    totalNames,
    setCurrentPage,
    currentPage,
}) => {
    
    const pageNumbers = [];

    for (let i = 1; i = Math.ceil(totalNames / namesPerPage); i++) {
        pageNumbers.push(i);
    }

    const paginate = (pageNumber, e) => {
        e.PreventDefault();
        setCurrentPage(pageNumber);
    };

    return (
        <nav>
            <ul className="pagination">
                {pageNumbers.map((number) => (
                    <li 
                        key={number}
                        className={`page-item ${currentPage === number ? "active" : ""}`}
                    >
                        <a
                            onClick={(e) => paginate(number, e)}
                            href="!#"
                            className="page-link"
                        >
                            {number}
                        </a>
                    </li>
                ))}
            </ul>
        </nav>
    );
}


export default Users;