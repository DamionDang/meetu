from django.db import models
from users.models import User

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255, db_index=True)  # 添加索引，用于按房间查询
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # 添加索引，用于查询用户消息
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)  # 添加索引，用于时间排序

    class Meta:
        indexes = [
            models.Index(fields=['room_name', '-timestamp'], name='chat_room_time_idx'),  # 房间+时间复合索引
            models.Index(fields=['user', '-timestamp'], name='chat_user_time_idx'),  # 用户+时间复合索引
        ]
        ordering = ['-timestamp']  # 默认按时间倒序

    def __str__(self):
        message_preview = str(self.message)[:20] if self.message else ''
        return f'{self.user} 在 {self.room_name} 中说: {message_preview}'
# Create your models here.
