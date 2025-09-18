from django.db import models
from users.models import User
from django.db.models import Q

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='sent_requests',
        on_delete=models.CASCADE,
        db_index=True  # 添加索引
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_requests',
        on_delete=models.CASCADE,
        db_index=True  # 添加索引
    )
    accepted = models.BooleanField(default=False, db_index=True)  # 添加索引，用于查询待处理请求
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # 添加索引

    class Meta:
        unique_together = ('from_user', 'to_user')
        indexes = [
            models.Index(fields=['to_user', 'accepted'], name='friend_req_to_accepted_idx'),  # 接收者+状态索引
            models.Index(fields=['from_user', 'accepted'], name='friend_req_from_accepted_idx'),  # 发送者+状态索引
            models.Index(fields=['-created_at'], name='friend_req_created_desc_idx'),  # 创建时间倒序
        ]

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({'Accepted' if self.accepted else 'Pending'})"

    def save(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValueError("发送失败!")
        super().save(*args, **kwargs)


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User,
        related_name='friends1',
        on_delete=models.CASCADE,
        db_index=True  # 添加索引
    )
    user2 = models.ForeignKey(
        User,
        related_name='friends2',
        on_delete=models.CASCADE,
        db_index=True  # 添加索引
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # 添加索引

    class Meta:
        unique_together = ('user1', 'user2')
        indexes = [
            models.Index(fields=['user1', 'user2'], name='friendship_users_idx'),  # 双向好友关系索引
            models.Index(fields=['-created_at'], name='friendship_created_desc_idx'),  # 创建时间倒序
        ]

    def __str__(self):
        return f"{self.user1} - {self.user2}"
