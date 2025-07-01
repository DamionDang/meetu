from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# 用户模型
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True

# 好友请求模型
class FriendRequestBase(BaseModel):
    from_user_id: int
    to_user_id: int

class FriendRequestCreate(FriendRequestBase):
    pass

class FriendRequest(FriendRequestBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

# 动态模型
class PostBase(BaseModel):
    content: str
    image_url: Optional[str] = None
    latitude: float
    longitude: float

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int
    user: User
    likes_count: int
    comments_count: int
    created_at: datetime

    class Config:
        orm_mode = True

# 点赞模型
class PostLikeBase(BaseModel):
    post_id: int
    user_id: int

class PostLikeCreate(PostLikeBase):
    pass

class PostLike(PostLikeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# 评论模型
class PostCommentBase(BaseModel):
    post_id: int
    user_id: int
    content: str

class PostCommentCreate(PostCommentBase):
    pass

class PostCommentResponse(PostCommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# 登录模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None