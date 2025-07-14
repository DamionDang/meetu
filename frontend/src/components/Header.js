// src/components/Header.js
import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header>
      <nav>
        <Link to="/">首页</Link>
        <Link to="/login">登录</Link>
        <Link to="/register">注册</Link>
      </nav>
    </header>
  );
}

export default Header;