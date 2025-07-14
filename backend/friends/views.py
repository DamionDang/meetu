from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from friends.models import FriendRequest,Friendship
from django.db.models import Q
from users.models import User
from friends.serializers import (
    SendFriendRequestSerializer,
    FriendRequestSerializer,
    AcceptFriendRequestSerializer,
    FriendshipSerializer
)

    
class SendFriendRequestView(APIView):
    def post(self, request):
        serializer = SendFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequestView(APIView):
    def post(self, request):
        serializer = AcceptFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            req = serializer.save()
            return Response(FriendRequestSerializer(req, context={'request': request}).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyFriendRequestsView(APIView):
    def get(self, request):
        requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        serializer = FriendRequestSerializer(requests, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyFriendsView(APIView):
    def get(self, request):
        friends = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        serializer = FriendshipSerializer(friends, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class SentFriendRequestsView(APIView):
    def get(self, request):
        requests = FriendRequest.objects.filter(from_user=request.user, accepted=False)
        serializer = FriendRequestSerializer(requests, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListFriendRequests(APIView):
    def get(self, request):
        user = request.user
        requests = FriendRequest.objects.filter(to_user=user, accepted=False)
        serializer = FriendRequestSerializer(requests, many=True)
        return Response(serializer.data)

# Create your views here.
