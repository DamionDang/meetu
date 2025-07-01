from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import User, FriendRequest, Friend, Post, PostLike, PostComment
from datetime import datetime
import asyncio
from websocket import manager  # 实时通知模块


# ========== 用户相关 ==========
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: dict):
    db_user = User(
        username=user["username"],
        email=user["email"],
        password_hash=user["password_hash"]
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_location(db: Session, user_id: int, latitude: float, longitude: float):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.latitude = latitude
        db_user.longitude = longitude
        db_user.geom = f"POINT({longitude} {latitude})"
        db.commit()
        db.refresh(db_user)
    return db_user


# ========== 好友请求相关 ==========
def send_friend_request(db: Session, from_user_id: int, to_user_id: int):
    existing = db.query(FriendRequest).filter(
        FriendRequest.from_user_id == from_user_id,
        FriendRequest.to_user_id == to_user_id
    ).first()
    if existing:
        return None  # 已存在请求

    db_request = FriendRequest(
        from_user_id=from_user_id,
        to_user_id=to_user_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def accept_friend_request(db: Session, request_id: int):
    db_request = db.query(FriendRequest).filter(FriendRequest.id == request_id).first()
    if db_request:
        db_request.status = "accepted"
        db.commit()

        # 创建双向好友关系
        friend1 = Friend(user_id=db_request.from_user_id, friend_id=db_request.to_user_id)
        friend2 = Friend(user_id=db_request.to_user_id, friend_id=db_request.from_user_id)

        db.add(friend1)
        db.add(friend2)
        db.commit()

    return db_request

def get_pending_requests(db: Session, user_id: int):
    return db.query(FriendRequest).filter(
        FriendRequest.to_user_id == user_id,
        FriendRequest.status == "pending"
    ).all()


# ========== 查看附近用户 ==========
def get_nearby_users(db: Session, user_id: int, radius_meters: int = 1000):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.geom:
        return []

    nearby_users = db.query(User).filter(
        User.id != user_id,
        func.ST_DWithin(User.geom, user.geom, radius_meters)
    ).all()
    return nearby_users


# ========== 动态相关 ==========
def create_post(db: Session, post_data: dict):
    db_post = Post(
        user_id=post_data["user_id"],
        content=post_data["content"],
        image_url=post_data.get("image_url"),
        latitude=post_data["latitude"],
        longitude=post_data["longitude"],
        geom=f"POINT({post_data['longitude']} {post_data['latitude']})"
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_nearby(db: Session, user_id: int, radius_meters: int = 1000):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.geom:
        return []

    posts = db.query(Post).filter(
        func.ST_DWithin(Post.geom, user.geom, radius_meters)
    ).order_by(Post.created_at.desc()).all()
    return posts

def get_posts_by_friends(db: Session, user_id: int):
    friends = db.query(Friend.friend_id).filter(Friend.user_id == user_id).all()
    friend_ids = [f[0] for f in friends]
    if not friend_ids:
        return []
    return db.query(Post).filter(Post.user_id.in_(friend_ids)).order_by(Post.created_at.desc()).all()


# ========== 点赞与评论 ==========
def like_post(db: Session, post_id: int, user_id: int):
    existing = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == user_id
    ).first()
    if existing:
        return None  # 已点赞

    db_like = PostLike(post_id=post_id, user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)

    # 异步通知作者
    asyncio.create_task(notify_liked_post(post_id, user_id, db))
    return db_like

async def notify_liked_post(post_id: int, user_id: int, db: Session):
    post = db.query(Post).get(post_id)
    if post:
        message = {
            "type": "like",
            "post_id": post_id,
            "user": db.query(User).get(user_id).username,
            "target_user": post.user.username,
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.send_notification(post.user_id, message)


def comment_on_post(db: Session, post_id: int, user_id: int, content: str):
    db_comment = PostComment(post_id=post_id, user_id=user_id, content=content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    # 异步通知作者
    asyncio.create_task(notify_commented_post(post_id, user_id, content, db))
    return db_comment

async def notify_commented_post(post_id: int, user_id: int, content: str, db: Session):
    post = db.query(Post).get(post_id)
    if post:
        message = {
            "type": "comment",
            "post_id": post_id,
            "user": db.query(User).get(user_id).username,
            "content": content[:30],
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.send_notification(post.user_id, message)


# ========== 实时通知 ==========
def notify_new_post(db_post, db: Session):
    # 获取该用户的关注者/好友
    friend_ids = [f.friend_id for f in db.query(Friend).filter(Friend.user_id == db_post.user_id)]
    for fid in friend_ids:
        message = {
            "type": "new_post",
            "post_id": db_post.id,
            "user": db_post.user.username,
            "content": db_post.content[:50],
            "timestamp": db_post.created_at.isoformat()
        }
        asyncio.create_task(manager.send_notification(fid, message))