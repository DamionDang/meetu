# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.friend_id = self.scope['url_route']['kwargs']['friend_id']

        await self.channel_layer.group_add(
            f"chat_{self.user_id}_{self.friend_id}",
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"chat_{self.user_id}_{self.friend_id}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            f"chat_{self.user_id}_{self.friend_id}",
            {
                "type": "chat_message",
                "message": data
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))