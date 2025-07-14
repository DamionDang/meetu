from django.urls import path
from posts.views import PostListView, CreatePostView,UserPostListView,PostDetailView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='post-create'),
    path('all/', PostListView.as_view(), name='post-list'),
    path('user/<int:user_id>/', UserPostListView.as_view(), name='user-posts'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
]