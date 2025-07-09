import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from users.models import CustomUser
from .models import ChatMessage  # 可选：消息记录

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 将用户加入该房间的组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 用户断开连接时离开房间
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # 接收到客户端发送的消息
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            user = self.scope.get('user')

            if not user.is_authenticated:
                await self.send(text_data=json.dumps({
                    'error': '未认证用户不能发送消息'
                }))
                return

            # 广播消息到房间组
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'timestamp': str(datetime.now())
                }
            )

            # 可选：保存消息到数据库
            try:
                await ChatMessage.objects.acreate(
                    room_name=self.room_name,
                    user=user,
                    message=message
                )
            except Exception as e:
                print("消息保存失败:", e)

    async def chat_message(self, event):
        # 收到组内广播的消息后转发给当前连接的客户端
        message = event.get('message')
        username = event.get('username')
        timestamp = event.get('timestamp')

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))