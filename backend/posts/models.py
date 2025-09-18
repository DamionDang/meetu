from django.db import models
from users.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # 添加索引，用于查询用户动态
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # 添加索引，用于时间排序

    class Meta:
        indexes = [
            models.Index(fields=['-created_at'], name='post_created_desc_idx'),  # 创建时间倒序索引
            models.Index(fields=['author', '-created_at'], name='post_author_time_idx'),  # 作者+时间复合索引
            models.Index(fields=['latitude', 'longitude'], name='post_location_idx'),  # 地理位置索引
        ]
        ordering = ['-created_at']  # 默认按创建时间倒序

    def __str__(self):
        return f"{self.author} 的动态"