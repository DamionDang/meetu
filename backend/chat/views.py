from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatHistoryView(APIView):
    def get(self, request, room_name):
        messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')[:50]
        serializer = ChatMessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)