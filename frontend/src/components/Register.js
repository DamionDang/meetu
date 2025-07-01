// src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';

const Register = ({ onRegisterSuccess }) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/register', {
                username,
                email,
                password
            });
            const { token, id: userId } = response.data;

            // 存储 token 和用户 ID
            localStorage.setItem('token', token);
            localStorage.setItem('userId', userId);

            // 注册成功回调
            onRegisterSuccess(userId);
        } catch (err) {
            setError("Registration failed");
        }
    };

    return (
        <div className="register-container">
            <h2>Register</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleRegister}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default Register;