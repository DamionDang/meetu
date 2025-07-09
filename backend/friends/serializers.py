from rest_framework import serializers
from users.serializers import UserSerializer
from .models import FriendRequest, Friendship
from users.models import User
from django.db.models import Q

class FriendRequestSerializer(serializers.ModelSerializer):
    from_username = UserSerializer(read_only=True)
    to_username = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user','from_username', 'to_user',  'to_username','accepted', 'created_at']
        read_only_fields = ['from_user','from_username', 'accepted', 'created_at']


    def get_from_username(self, obj):
        return obj.from_user.username

    def get_to_username(self, obj):
        return obj.to_user.username
    
class SendFriendRequestSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField()

    def validate_to_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        return user

    def create(self, validated_data):
        from_user = self.context['request'].user
        to_user = validated_data['to_user_id']

        if from_user == to_user:
            raise serializers.ValidationError({"error": "不能添加自己为好友"})

        existing_request = FriendRequest.objects.filter(
            Q(from_user=from_user, to_user=to_user) |
            Q(from_user=to_user, to_user=from_user)
        ).first()

        if existing_request:
            if existing_request.accepted:
                raise serializers.ValidationError({"error": "你们已经是好友了"})
            elif existing_request.from_user == from_user:
                raise serializers.ValidationError({"error": "你已经发送过好友请求"})
            else:
                raise serializers.ValidationError({"error": "对方已向你发送过请求，请先处理"})

        return FriendRequest.objects.create(
            from_user=from_user,
            to_user=to_user
        )


class AcceptFriendRequestSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()

    def validate_request_id(self, value):
        try:
            req = FriendRequest.objects.get(id=value)
        except FriendRequest.DoesNotExist:
            raise serializers.ValidationError("请求不存在")

        if req.accepted:
            raise serializers.ValidationError("该请求已被处理")
        if req.to_user != self.context['request'].user:
            raise serializers.ValidationError("无权操作")

        return req

    def create(self, validated_data):
        req = validated_data['request_id']
        req.accepted = True
        req.save()

        Friendship.objects.create(user1=req.from_user, user2=req.to_user)

        return req


class FriendshipSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created_at']

    def get_friend(self, obj):
        user = self.context['request'].user
        if obj.user1 == user:
            return UserSerializer(obj.user2).data
        else:
            return UserSerializer(obj.user1).data