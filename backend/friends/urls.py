from django.urls import path
from .views import (
    SendFriendRequestView,
    AcceptFriendRequestView,
    MyFriendRequestsView,
    SentFriendRequestsView,
    MyFriendsView,
    ListFriendRequests
)

urlpatterns = [
    path('requests', ListFriendRequests.as_view(), name='list-requests'),
    path('send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('accept/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('received/', MyFriendRequestsView.as_view(), name='my-received-requests'),
    path('sent/', SentFriendRequestsView.as_view(), name='my-sent-requests'),
    path('my/', MyFriendsView.as_view(), name='my-friends'),
]