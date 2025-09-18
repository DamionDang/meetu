# utils/cache.py
from django.core.cache import caches
from django.conf import settings
import json
import hashlib
import logging
from functools import wraps
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_alias='default'):
        self.cache = caches[cache_alias]
    
    def get(self, key: str, default=None) -> Any:
        """获取缓存"""
        try:
            return self.cache.get(key, default)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return default
    
    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """设置缓存"""
        try:
            return self.cache.set(key, value, timeout)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            return self.cache.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def get_or_set(self, key: str, default_func, timeout: Optional[int] = None) -> Any:
        """获取缓存，如果不存在则调用函数设置"""
        try:
            result = self.cache.get(key)
            if result is None:
                result = default_func()
                if result is not None:
                    self.cache.set(key, result, timeout)
            return result
        except Exception as e:
            logger.error(f"Cache get_or_set error for key {key}: {e}")
            return default_func()

# 全局缓存管理器实例
default_cache = CacheManager('default')
api_cache = CacheManager('api_cache')


def cache_key_generator(*args, **kwargs) -> str:
    """生成缓存键"""
    key_data = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(key_data.encode()).hexdigest()


def cached_api(timeout: int = 300, cache_alias: str = 'api_cache', key_prefix: str = ''):
    """API缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{cache_key_generator(*args, **kwargs)}"
            
            cache_manager = CacheManager(cache_alias)
            
            # 尝试从缓存获取
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for key: {cache_key}")
                return cached_result
            
            # 执行原函数
            result = func(*args, **kwargs)
            
            # 存储到缓存
            if result is not None:
                cache_manager.set(cache_key, result, timeout)
                logger.info(f"Cache set for key: {cache_key}")
            
            return result
        return wrapper
    return decorator


class UserCacheManager:
    """用户相关缓存管理"""
    
    @staticmethod
    def get_user_profile_key(user_id: int) -> str:
        return f"user:profile:{user_id}"
    
    @staticmethod
    def get_user_friends_key(user_id: int) -> str:
        return f"user:friends:{user_id}"
    
    @staticmethod
    def get_user_posts_key(user_id: int, page: int = 1) -> str:
        return f"user:posts:{user_id}:page:{page}"
    
    @staticmethod
    def invalidate_user_cache(user_id: int):
        """清除用户相关缓存"""
        keys_to_delete = [
            UserCacheManager.get_user_profile_key(user_id),
            UserCacheManager.get_user_friends_key(user_id),
        ]
        
        for key in keys_to_delete:
            default_cache.delete(key)
        
        # 清除用户动态缓存（多页）
        for page in range(1, 6):  # 清除前5页缓存
            post_key = UserCacheManager.get_user_posts_key(user_id, page)
            default_cache.delete(post_key)


class PostCacheManager:
    """动态相关缓存管理"""
    
    @staticmethod
    def get_feed_key(user_id: int, page: int = 1) -> str:
        return f"feed:{user_id}:page:{page}"
    
    @staticmethod
    def get_post_detail_key(post_id: int) -> str:
        return f"post:detail:{post_id}"
    
    @staticmethod
    def invalidate_feed_cache(user_id: int):
        """清除用户动态流缓存"""
        for page in range(1, 6):  # 清除前5页缓存
            feed_key = PostCacheManager.get_feed_key(user_id, page)
            default_cache.delete(feed_key)
    
    @staticmethod
    def invalidate_post_cache(post_id: int):
        """清除特定动态缓存"""
        post_key = PostCacheManager.get_post_detail_key(post_id)
        default_cache.delete(post_key)


class ChatCacheManager:
    """聊天相关缓存管理"""
    
    @staticmethod
    def get_room_messages_key(room_name: str, page: int = 1) -> str:
        return f"chat:room:{room_name}:page:{page}"
    
    @staticmethod
    def get_user_conversations_key(user_id: int) -> str:
        return f"chat:conversations:{user_id}"
    
    @staticmethod
    def invalidate_room_cache(room_name: str):
        """清除聊天室缓存"""
        for page in range(1, 6):  # 清除前5页缓存
            room_key = ChatCacheManager.get_room_messages_key(room_name, page)
            default_cache.delete(room_key)
    
    @staticmethod
    def invalidate_user_conversations(user_id: int):
        """清除用户会话列表缓存"""
        conv_key = ChatCacheManager.get_user_conversations_key(user_id)
        default_cache.delete(conv_key)