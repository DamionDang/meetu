from fastapi import FastAPI, Depends, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
import models
import database
import websocket

app = FastAPI()

# 初始化数据库
models.Base.metadata.create_all(bind=database.engine)

# 允许跨域请求（前端 React 使用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== WebSocket 实时通知 ==========
@app.websocket("/notifications/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    websocket.client_state = {"user_id": user_id}
    websocket_manager.connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # 可处理客户端发送的消息（如“已读通知”）
    except Exception as e:
        del websocket_manager.connections[user_id]

websocket_manager = websocket.NotificationManager()


# ========== 用户相关接口 ==========
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user.dict())

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if not db_user or db_user.password_hash != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {
        "id": db_user.id,
        "username": db_user.username,
        "token": f"fake-jwt-token-{db_user.id}"
    }


# ========== 地理位置更新 ==========
@app.post("/location")
def update_location(user_id: int, latitude: float, longitude: float, db: Session = Depends(database.get_db)):
    return crud.update_user_location(db, user_id, latitude, longitude)


# ========== 好友系统 ==========
@app.post("/friend-requests")
def send_request(from_user_id: int, to_user_id: int, db: Session = Depends(database.get_db)):
    return crud.send_friend_request(db, from_user_id, to_user_id)

@app.post("/friend-requests/{request_id}/accept")
def accept_request(request_id: int, db: Session = Depends(database.get_db)):
    return crud.accept_friend_request(db, request_id)

@app.get("/friend-requests/{user_id}", response_model=List[schemas.FriendRequest])
def get_pending_requests(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_pending_requests(db, user_id)


# ========== 查看附近用户 ==========
@app.get("/nearby-users/{user_id}")
def get_nearby_users(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_nearby_users(db, user_id)


# ========== 动态功能 ==========
@app.post("/posts", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(database.get_db)):
    post_data = post.dict()
    post_data["user_id"] = user_id
    db_post = crud.create_post(db, post_data)
    crud.notify_new_post(db_post, db)  # 推送新动态通知
    return db_post

@app.get("/posts/nearby", response_model=List[schemas.PostResponse])
def get_nearby_posts(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_posts_nearby(db, user_id)

@app.get("/posts/friends", response_model=List[schemas.PostResponse])
def get_friends_posts(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_posts_by_friends(db, user_id)


# ========== 点赞与评论 ==========
@app.post("/posts/{post_id}/like")
def like_post(post_id: int, user_id: int, db: Session = Depends(database.get_db)):
    return crud.like_post(db, post_id, user_id)

@app.post("/posts/{post_id}/comment")
def comment_on_post(post_id: int, user_id: int, content: str, db: Session = Depends(database.get_db)):
    return crud.comment_on_post(db, post_id, user_id, content)