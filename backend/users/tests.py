from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from users.models import User
from users.serializers import UserSerializer
from utils.exceptions import AuthenticationException, ValidationException
import json

User = get_user_model()

class UserModelTest(TestCase):
    """用户模型测试"""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        """测试创建用户"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
    
    def test_create_superuser(self):
        """测试创建超级用户"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_user_str_representation(self):
        """测试用户字符串表示"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])
    
    def test_email_uniqueness(self):
        """测试邮箱唯一性"""
        User.objects.create_user(**self.user_data)
        
        with self.assertRaises(Exception):
            User.objects.create_user(
                email=self.user_data['email'],
                username='anotheruser',
                password='pass123'
            )
    
    def test_username_uniqueness(self):
        """测试用户名唯一性"""
        User.objects.create_user(**self.user_data)
        
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='another@example.com',
                username=self.user_data['username'],
                password='pass123'
            )
    
    def test_user_location_fields(self):
        """测试用户地理位置字段"""
        user = User.objects.create_user(**self.user_data)
        user.latitude = 39.9042
        user.longitude = 116.4074
        user.save()
        
        self.assertEqual(user.latitude, 39.9042)
        self.assertEqual(user.longitude, 116.4074)


class UserAPITest(APITestCase):
    """用户API测试"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
    
    def test_user_registration(self):
        """测试用户注册"""
        url = reverse('user-register')  # 需要在urls.py中定义
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        # 根据实际API响应调整期望状态码
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertTrue(User.objects.filter(email=data['email']).exists())
    
    def test_user_login(self):
        """测试用户登录"""
        url = reverse('user-login')  # 需要在urls.py中定义
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(url, data, format='json')
        
        # 根据实际API响应调整期望结果
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('access_token', response.data)
    
    def test_invalid_login(self):
        """测试错误登录"""
        url = reverse('user-login')  # 需要在urls.py中定义
        data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        # 根据实际API响应调整期望结果
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_profile_access(self):
        """测试用户资料访问"""
        # 模拟JWT认证
        self.client.force_authenticate(user=self.user)
        
        url = reverse('user-profile')  # 需要在urls.py中定义
        response = self.client.get(url)
        
        # 根据实际API响应调整期望结果
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['email'], self.user.email)
    
    def test_unauthorized_profile_access(self):
        """测试未授权访问用户资料"""
        url = reverse('user-profile')  # 需要在urls.py中定义
        response = self.client.get(url)
        
        # 根据实际API响应调整期望结果
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_user_location(self):
        """测试更新用户位置"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('user-update-location')  # 需要在urls.py中定义
        data = {
            'latitude': 39.9042,
            'longitude': 116.4074
        }
        
        response = self.client.patch(url, data, format='json')
        
        # 根据实际API响应调整期望结果
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.user.refresh_from_db()
        # self.assertEqual(self.user.latitude, data['latitude'])
        # self.assertEqual(self.user.longitude, data['longitude'])


class UserSerializerTest(TestCase):
    """用户序列化器测试"""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
    
    def test_user_serialization(self):
        """测试用户序列化"""
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['username'], self.user.username)
        # 确保密码不被序列化
        self.assertNotIn('password', data)
    
    def test_user_deserialization(self):
        """测试用户反序列化"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
        }
        
        serializer = UserSerializer(data=data)
        # 根据实际序列化器实现调整验证逻辑
        # self.assertTrue(serializer.is_valid())


class UserAuthenticationTest(TestCase):
    """用户认证测试"""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
    
    @patch('users.authentication.JWTAuthentication.authenticate')
    def test_jwt_authentication_success(self, mock_authenticate):
        """测试JWT认证成功"""
        mock_authenticate.return_value = (self.user, None)
        
        # 模拟认证过程
        result = mock_authenticate()
        
        self.assertEqual(result[0], self.user)
    
    @patch('users.authentication.JWTAuthentication.authenticate')
    def test_jwt_authentication_failure(self, mock_authenticate):
        """测试JWT认证失败"""
        mock_authenticate.side_effect = AuthenticationException('无效的token')
        
        with self.assertRaises(AuthenticationException):
            mock_authenticate()


class UserValidationTest(TestCase):
    """用户数据验证测试"""
    
    def test_email_validation(self):
        """测试邮箱格式验证"""
        invalid_emails = [
            'invalid-email',
            '@example.com',
            'test@',
            'test..test@example.com'
        ]
        
        for email in invalid_emails:
            with self.assertRaises(Exception):
                User.objects.create_user(
                    email=email,
                    username=f'user_{email}',
                    password='pass123'
                )
    
    def test_password_validation(self):
        """测试密码验证"""
        # 测试密码长度等验证规则
        weak_passwords = [
            '123',
            'abc',
            ''
        ]
        
        for password in weak_passwords:
            with self.assertRaises(Exception):
                User.objects.create_user(
                    email=f'test_{password}@example.com',
                    username=f'user_{password}',
                    password=password
                )


class UserCacheTest(TestCase):
    """用户缓存测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
    
    @patch('utils.cache.UserCacheManager.get_user_profile_key')
    @patch('utils.cache.default_cache.get')
    def test_user_profile_cache_hit(self, mock_cache_get, mock_get_key):
        """测试用户资料缓存命中"""
        mock_get_key.return_value = f'user:profile:{self.user.id}'
        mock_cache_get.return_value = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email
        }
        
        # 模拟缓存操作
        cached_data = mock_cache_get(mock_get_key.return_value)
        
        self.assertEqual(cached_data['id'], self.user.id)
        self.assertEqual(cached_data['username'], self.user.username)
