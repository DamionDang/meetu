from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import Geography
from datetime import datetime
from sqlalchemy import func

# 用户表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(128))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    geom = Column(Geography("POINT", 4326))  # PostGIS 地理位置字段
    created_at = Column(DateTime, default=datetime.utcnow)

# 好友请求表
class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])

# 好友关系表
class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    friend_id = Column(Integer, ForeignKey("users.id"))

# 动态表
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(500))
    image_url = Column(String(255), nullable=True)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    geom = Column(Geography("POINT", 4326))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id])
    likes = relationship("PostLike")
    comments = relationship("PostComment")

# 动态点赞表
class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", foreign_keys=[post_id])
    user = relationship("User", foreign_keys=[user_id])

# 动态评论表
class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", foreign_keys=[post_id])
    user = relationship("User", foreign_keys=[user_id])