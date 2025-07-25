import React, { useState } from 'react';



const Pagination = ({namesPerPage, totalNames, setCurrentPage, currentPage }) => {
   
    const pageNumbers = [];

    for (let i = 1; i <= Math.ceil(totalNames / namesPerPage); i++) {
        pageNumbers.push(i);
    }

    const paginate = (pageNumber, e) => {
        e.preventDefault();
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
                            href="!#"
                            onClick={(e) => paginate(number, e)}
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

export default Pagination;