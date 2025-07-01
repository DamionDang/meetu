// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// 页面组件
import HomePage from './pages/HomePage';
import Login from './components/Login';
import Register from './components/Register';

// 布局组件
import Layout from './components/Layout';

const App = () => {
    // 从 localStorage 获取用户 ID 和 token
    const [userId, setUserId] = useState(localStorage.getItem('userId'));
    const [token, setToken] = useState(localStorage.getItem('token'));

    // 登录成功回调
    const handleLoginSuccess = (userId) => {
        setUserId(userId);
        localStorage.setItem('userId', userId);
    };

    // 注册成功回调
    const handleRegisterSuccess = (userId) => {
        setUserId(userId);
        localStorage.setItem('userId', userId);
    };

    // 登出逻辑
    const handleLogout = () => {
        setUserId(null);
        setToken(null);
        localStorage.removeItem('userId');
        localStorage.removeItem('token');
    };

    return (
        <Router>
            <Routes>
                {/* 公共路由 */}
                <Route path="/login" element={!userId ? <Login onLoginSuccess={handleLoginSuccess} /> : <Navigate to="/" />} />
                <Route path="/register" element={!userId ? <Register onRegisterSuccess={handleRegisterSuccess} /> : <Navigate to="/" />} />
                // src/App.js
                <Route path="/friends/:id" element={userId ? <FriendDetailPage userId={userId} /> : <Navigate to="/login" />} />
                {/* 受保护的路由 */}
                <Route path="/" element={userId ? <Layout onLogout={handleLogout} userId={userId} /> : <Navigate to="/login" />} />
            </Routes>
        </Router>
    );
};

export default App;