import {useState} from "react";

const Hamburger = () => {
    const [activeMenu, setActiveMenu] = useState(false);
    return (
        <div className="hamburger-menu">
            <button
                className={`hamburger-button ${activeMenu ? "active" : ""}`}
                onClick={() => setActiveMenu(!activeMenu)}
            >
                <span className="bar"></span>
                <span className="bar"></span>
                <span className="bar"></span>
            </button>
            {activeMenu && (
                <div className="menu">
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/about">About</a></li>
                        <li><a href="/contact">Contact</a></li>
                    </ul>
                </div>
            )}
        </div>
    );

}