// src/components/BottomNav.js
import React from 'react';
import { Link } from 'react-router-dom';

const BottomNav = () => {
    return (
        <nav style={{
            position: "fixed",
            bottom: 0,
            width: "100%",
            backgroundColor: "#282c34",
            display: "flex",
            justifyContent: "space-around",
            padding: "10px 0",
            color: "white",
            boxShadow: "0 -2px 5px rgba(0,0,0,0.1)",
            zIndex: 1000
        }}>
            <Link to="/" style={{ textAlign: "center", color: "white" }}>
                <span role="img" aria-label="home">🏠</span>
                <div>Home</div>
            </Link>
            <Link to="/friends" style={{ textAlign: "center", color: "white" }}>
                <span role="img" aria-label="friends">👥</span>
                <div>Friends</div>
            </Link>
            <Link to="/notifications" style={{ textAlign: "center", color: "white" }}>
                <span role="img" aria-label="notifications">🔔</span>
                <div>Notifications</div>
            </Link>
            <Link to="/profile" style={{ textAlign: "center", color: "white" }}>
                <span role="img" aria-label="profile">👤</span>
                <div>Profile</div>
            </Link>
        </nav>
    );
};

export default BottomNav;