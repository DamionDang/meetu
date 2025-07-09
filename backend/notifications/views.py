from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer, MarkAsReadSerializer

class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAsReadView(APIView):
    def post(self, request):
        serializer = MarkAsReadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            notification = serializer.update(serializer.validated_data['notification_id'], {})
            return Response(NotificationSerializer(notification, context={'request': request}).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)