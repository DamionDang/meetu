from rest_framework import serializers
from ..posts.models import Post
from users.models import User
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'content', 'image', 'latitude', 'longitude', 'created_at']
        read_only_fields = ['user', 'created_at']

    def get_author_username(self, obj):
        return obj.author.username
        

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'image', 'latitude']

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(user=user, **validated_data)