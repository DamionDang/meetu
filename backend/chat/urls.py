from django.urls import path
from chat.views import ChatHistoryView

urlpatterns = [
    path('history/<str:room_name>/', ChatHistoryView.as_view(), name='chat-history'),
]
