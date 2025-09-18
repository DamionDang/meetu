from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer
from utils.cache import cached_api, ChatCacheManager, api_cache
from utils.exceptions import StandardResponse
import logging

logger = logging.getLogger('chat')

class ChatHistoryView(APIView):
    @cached_api(timeout=300, key_prefix='chat_history')
    def get(self, request, room_name):
        """获取聊天历史记录（带缓存）"""
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 50))
            
            # 计算偏移量
            offset = (page - 1) * page_size
            
            # 查询消息
            messages = ChatMessage.objects.filter(
                room_name=room_name
            ).select_related('user').order_by('-timestamp')[offset:offset + page_size]
            
            serializer = ChatMessageSerializer(
                messages, 
                many=True, 
                context={'request': request}
            )
            
            logger.info(f"Chat history loaded for room {room_name}, page {page}")
            
            return StandardResponse.success(
                data={
                    'messages': serializer.data,
                    'page': page,
                    'has_more': len(messages) == page_size
                },
                message="聊天记录获取成功"
            )
            
        except Exception as e:
            logger.error(f"Error loading chat history for room {room_name}: {e}")
            return StandardResponse.error(
                message="获取聊天记录失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )