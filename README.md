# 🌟 MEETU Network App

> MEETU是一个基于现代 Web 技术栈构建的社交网络应用，支持用户登录、发布动态、好友系统、实时聊天与地图定位等功能。

---

## 🧩 项目简介

MEETU是一个基于现代 Web 技术栈构建的社交网络应用，采用**前后端分离架构**设计。项目实现了完整的社交平台核心功能，包括用户认证、动态发布、好友系统、实时聊天和地理位置服务。前端使用 **React** 构建，后端使用 **Django + DRF + Channels** 提供 API 接口和 WebSocket 实时通信。

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
│   ├── notifications/  # 通知系统模块
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
npm start
```

#### 后端：
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. API文档访问
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- 日志文件: `backend/logs/`

---

## 🚀 性能优化与代码改进

### ✅ 已完成的优化

#### 代码改进：
1. **统一异常处理机制** - 实现自定义异常类和全局异常处理器
2. **生产级别日志系统** - 配置结构化日志、轮转日志和安全日志
3. **测试用例覆盖** - 为核心模块添加全面的单元测试和集成测试
4. **自动化API文档** - 集成drf-spectacular生成Swagger/ReDoc文档

#### 性能优化：
1. **数据库索引优化** - 为高频查询字段添加单列和复合索引
2. **Redis缓存策略** - 实现多层缓存架构和缓存管理器
3. **前端代码分割** - 实现路由懒加载和组件懒加载
4. **CDN静态文件服务** - 配置生产环境CDN和静态资源优化

### 🎆 技术亮点

- **全局异常处理**: 统一的API响应格式和错误码管理
- **结构化日志**: 支持JSON格式、轮转日志和分类记录
- **智能缓存**: 支持缓存装饰器、自动无效化和分层缓存
- **响应式组件**: 支持虚拟滚动、错误边界和加载状态
- **数据库优化**: 精心设计的复合索引和查询优化
- **全面测试**: 单元测试、集成测试和WebSocket测试覆盖
## 📬 联系作者

如有任何问题或建议，请联系我：
📮[dangruizhi66@163.com]
WeChat：![image](https://github.com/user-attachments/assets/68c0d8f2-6fa5-4a91-b069-7dfafd096f6c)

