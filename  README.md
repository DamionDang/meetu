map-social-full-project/
│
├── backend/               # FastAPI 后端
│   ├── main.py            # 主程序入口
│   ├── models.py          # 数据库模型
│   ├── schemas.py         # Pydantic 模型
│   ├── crud.py            # 数据操作逻辑
│   ├── database.py        # 数据库连接
│   ├── websocket.py       # WebSocket 实时通知
│   └── .env.example       # 环境变量示例
│
├─frontend/                       # 项目根目录
├── public/                      # 静态资源目录（不参与编译）
│   └── index.html               # 主 HTML 页面，React 渲染入口
│
├── src/                         # 源码目录，所有 React 组件和逻辑代码都放在这里
│   ├── App.js                   # React 路由主组件，定义整个应用的路由配置
│   ├── index.js                 # 应用入口文件，创建 ReactDOM 并挂载到 #root
│   ├── index.css                # 全局样式文件，重置默认样式、设置基础样式
│
│   ├── components/              # 可复用的 UI 组件目录
│   │   ├── Login.js             # 登录页组件，支持动画过渡效果
│   │   ├── Register.js          # 注册页组件，用户注册表单
│   │   ├── Layout.js            # 页面布局组件，包含头部、内容区域和底部导航
│   │   ├── MapComponent.js      # 地图组件，集成 Google Maps 显示位置信息
│   │   ├── PostFeed.js          # 动态流展示组件，用于显示用户发布的动态列表
│   │   ├── Notification.js      # 通知组件，通过 WebSocket 接收实时通知
│   │   ├── ChatWindow.js        # 实时聊天窗口组件，使用 WebSocket 进行消息通信
│   │   ├── FriendRequestList.js # 好友请求列表组件，展示收到的好友请求
│   │   ├── FriendsList.js       # 好友列表组件，展示当前用户的所有好友
│   │   ├── GeolocationButton.js # 获取当前位置按钮组件，调用浏览器定位 API
│   │   ├── CreatePostForm.js    # 发布动态表单组件，支持文字+图片+地理位置上传
│   │   ├── BottomNav.js         # 移动端底部导航栏组件，适配手机屏幕
│   │   ├── SearchUserPage.js    # 用户搜索页面，支持按用户名或邮箱查找用户
│   │   └── ...                  # 其他小型组件如按钮、弹窗等可继续添加
│
│   ├── pages/                   # 页面级组件目录（通常与路由对应）
│   │   ├── HomePage.js          # 首页，展示动态流、地图、通知等综合信息
│   │   ├── FriendDetailPage.js  # 好友详情页，打开后进入一对一聊天界面
│   │   └── ProfilePage.js       # 用户资料页，展示个人信息和发布过的动态
│
│   └── utils/                   # 工具类或通用函数目录
│       └── api.js               # 封装 Axios 请求，统一管理 API 接口调用（可选）
│
├── package.json                 # 项目依赖和脚本命令配置文件
└── .env                         # 环境变量配置文件（如 API 地址、Google Maps Key）
│
├── migrations/            # Alembic 数据库迁移脚本
├── docker-compose.yml     # Docker 部署配置
└── README.md              # 使用说明和接口文档

’‘’
.
├── backend/                  # Django 后端
│   ├── config/               # Django 项目配置
│   │   ├── __init__.py
│   │   ├── asgi.py           # WebSocket 支持
│   │   ├── settings.py       # 全局设置
│   │   ├── urls.py           # 主路由
│   │   └── wsgi.py           # 部署入口
│   │
│   ├── users/                # 用户系统模块
│   │   ├── models.py         # 用户模型
│   │   ├── views.py          # 登录 / 注册接口
│   │   ├── serializers.py    # 序列化器
│   │   ├── authentication.py # JWT 认证逻辑
│   │   └── urls.py           # 路由
│   │
│   ├── posts/                # 动态发布模块
│   │   ├── models.py         # 动态模型
│   │   ├── views.py          # 接口视图
│   │   ├── serializers.py    # 序列化器
│   │   └── urls.py           # 路由
│   │
│   ├── friends/              # 好友关系模块
│   │   ├── models.py         # 好友请求模型
│   │   ├── views.py          # 接口视图
│   │   ├── serializers.py    # 序列化器
│   │   └── urls.py           # 路由
│   │
│   ├── chat/                 # 实时聊天模块
│   │   ├── consumers.py      # WebSocket 消费者
│   │   ├── routing.py        # WebSocket 路由
│   │   └── apps.py
│   │
│   ├── notifications/        # 通知系统模块（新增）
│   │   ├── models.py         # 通知模型
│   │   ├── views.py          # 接口视图
│   │   ├── serializers.py    # 序列化器
│   │   ├── urls.py           # 路由
│   │   └── utils.py          # 工具函数（WebSocket 推送）
│   │
│   ├── manage.py             # Django 管理脚本
│   ├── requirements.txt      # Python 依赖包列表
│   └── .gitignore            # Git 忽略文件
│
├── frontend/                 # React 前端项目
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/       # 可复用组件
│   │   │   ├── Header.jsx
│   │   │   ├── PostForm.jsx
│   │   │   ├── ChatBox.jsx
│   │   │   └── NotificationItem.jsx
│   │   │
│   │   ├── pages/            # 页面组件
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Feed.jsx
│   │   │   ├── Friends.jsx
│   │   │   └── Chat.jsx
│   │   │
│   │   ├── hooks/            # 自定义 Hooks
│   │   │   └── useWebSocket.js
│   │   │
│   │   ├── services/         # API 请求封装
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx           # 根组件
│   │   └── main.jsx          # 入口文件
│   │
│   ├── package.json
│   ├── .env                  # 环境变量
│   └── README.md             # React 默认说明文档
│
├── media/                    # 用户上传的媒体文件（如图片）
│   └── uploads/
│       └── posts/
│           └── 2025/
│               └── 07/
│                   └── 02/
│                       └── image.jpg
│
├── .gitignore
└── README.md                 # 项目总说明文档
‘’‘