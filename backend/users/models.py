from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('必须提供邮箱')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)  # 添加索引，用于登录查询
    username = models.CharField(max_length=150, unique=True, db_index=True)  # 添加索引，用于搜索
    is_active = models.BooleanField(default=True, db_index=True)  # 添加索引，用于筛选活跃用户
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)  # 添加索引，用于时间范围查询
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude'], name='user_location_idx'),  # 地理位置复合索引
            models.Index(fields=['email', 'is_active'], name='user_email_active_idx'),  # 邮箱活跃状态复合索引
            models.Index(fields=['-date_joined'], name='user_date_joined_desc_idx'),  # 注册时间倒序索引
        ]

    def __str__(self):
        return self.username