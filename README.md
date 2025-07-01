# 🌟 Social Network App

> 基于 React 和 Django 的社交网络应用，支持用户登录、发布动态、好友系统、实时聊天与地图定位等功能。

---

## 🧩 项目简介

这是一个完整的社交网络类 Web 应用项目，前端使用 **React** 构建，后端使用 **Django + DRF + Channels** 提供 API 接口和 WebSocket 实时通信。项目采用 **前后端分离架构**，可独立部署。

---

## 📦 技术栈

| 类型 | 技术 |
|------|------|
| 前端 | React, Axios, react-router-dom, react-transition-group, Google Maps API |
| 后端 | Django, DRF, JWT 认证, Django Channels |
| 数据库 | SQLite (开发) / PostgreSQL (生产) |
| 实时通信 | WebSocket + Redis Channel Layer |
| 部署 | Nginx, Gunicorn, Docker（可选） |

---

## 📁 项目结构
```
.
├── frontend/           # React 前端项目
│   ├── public/
│   ├── src/
│   │   ├── components/ # 可复用组件
│   │   ├── pages/      # 页面级组件
│   │   └── utils/      # 工具函数和 API 封装
│   ├── package.json
│   └── .env
│
├── backend/            # Django 后端项目
│   ├── config/         # Django 设置文件
│   ├── users/          # 用户模块
│   ├── posts/          # 动态发布模块
│   ├── friends/        # 好友关系模块
│   ├── chat/           # 聊天与通知模块
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```
---

## 🔧 功能模块

### ✅ 前端功能

- 登录 / 注册页面（带动画过渡）
- 发布动态（支持文字+图片+地理位置）
- 地图集成（Google Maps 显示当前位置和好友位置）
- 好友搜索与添加
- 实时聊天（WebSocket 支持）
- 实时通知系统
- 移动端适配（响应式布局）

### ✅ 后端功能

- JWT Token 用户认证
- 用户注册与登录接口
- 动态发布与获取接口
- 好友关系管理（请求、接受、删除）
- WebSocket 聊天与通知系统
- 地理位置数据存储与检索

---

## 🚀 开发环境搭建指南

### 1. 安装依赖

#### 前端：

```bash
cd frontend
npm install
```

#### 后端：
```bash
cd backend
pip install -r requirements.txt
```
## 📬 联系作者

如有任何问题或建议，请联系我：
📮[dangruizhi66@163.com]
WeChat：![image](https://github.com/user-attachments/assets/68c0d8f2-6fa5-4a91-b069-7dfafd096f6c)

