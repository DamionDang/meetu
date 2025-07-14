from rest_framework import serializers
from notifications.models import Notification
from users.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'read', 'created_at']
        read_only_fields = ['user', 'title', 'message', 'created_at']


class MarkAsReadSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField()

    def validate_notification_id(self, value):
        try:
            notification = Notification.objects.get(id=value)
        except Notification.DoesNotExist:
            raise serializers.ValidationError("通知不存在")
        if notification.read:
            raise serializers.ValidationError("该通知已读")
        if notification.user != self.context['request'].user:
            raise serializers.ValidationError("无权操作")
        return notification

    def update(self, instance, validated_data):
        instance.read = True
        instance.save()
        return instance