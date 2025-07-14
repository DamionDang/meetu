// src/pages/LoginPage.js
import React from 'react';
import Login from '../components/Login';

function LoginPage() {
  const handleLogin = () => {
    alert('登录成功');
  };

  return (
    <div>
      <h2>登录</h2>
      <Login onLogin={handleLogin} />
    </div>
  );
}

export default LoginPage;