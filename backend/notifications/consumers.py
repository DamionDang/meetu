import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_group_name = f'notifications_{self.user.id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event['message']
        title = event['title']

        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': title,
            'message': message,
            'timestamp': str(timezone.now())
        }))