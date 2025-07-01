from fastapi import WebSocket
from typing import Dict

class NotificationManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = {}

    async def send_notification(self, user_id: int, message: dict):
        if user_id in self.connections:
            websocket = self.connections[user_id]
            try:
                await websocket.send_json(message)
            except Exception as e:
                # 连接异常时移除
                del self.connections[user_id]

# 实例化一个全局的通知管理器
manager = NotificationManager()