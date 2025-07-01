// src/components/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { CSSTransition } from 'react-transition-group';
import './Login.css'; // 动画样式

const Login = ({ onLoginSuccess }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [inProp, setInProp] = useState(false);

    useEffect(() => {
        setInProp(true);
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/auth/login', { email, password });
            localStorage.setItem('token', res.data.token);
            localStorage.setItem('userId', res.data.user_id);
            onLoginSuccess(res.data.user_id);
            navigate('/');
        } catch (err) {
            setError("Invalid email or password");
        }
    };

    return (
        <div className="login-container">
            <CSSTransition in={inProp} timeout={500} classNames="fade" unmountOnExit>
                <form onSubmit={handleSubmit} className="login-form">
                    <h2>Login</h2>
                    {error && <p className="error">{error}</p>}
                    <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    <button type="submit">Login</button>
                    <p>Don't have an account? <a href="/register">Register</a></p>
                </form>
            </CSSTransition>
        </div>
    );
};

export default Login;