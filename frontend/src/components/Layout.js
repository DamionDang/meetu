// src/components/Layout.js
import React from 'react';
import { Outlet, Link } from 'react-router-dom';

const Layout = ({ userId, onLogout }) => {
    return (
        <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
            {/* 顶部导航栏 */}
            <header style={{
                backgroundColor: "#282c34",
                color: "white",
                padding: "1rem",
                display: "flex",
                justifyContent: "space-between"
            }}>
                <h2>MapSocial</h2>
                <nav>
                    <Link to="/" style={{ margin: "0 1rem", color: "white" }}>Home</Link>
                    <button onClick={onLogout} style={{ background: "none", border: "none", color: "white", cursor: "pointer" }}>
                        Logout
                    </button>
                </nav>
            </header>

            {/* 页面主体内容 */}
            <main style={{ flex: 1, display: "flex" }}>
                <Outlet /> {/* 这里会渲染当前路径的页面组件 */}
            </main>
        </div>
    );
};

export default Layout;