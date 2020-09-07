from django.urls import path
from .views import (
    PostListAPIView,
    # UserPostListApiView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostCreateAPIView,
    PostLikeApiView,
    CommentCreateApiView,
)

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='detail'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('like-post/', PostLikeApiView.as_view(), name='like_post'),
    # path('<str:username>/', PostListAPIView.as_view(), name='user_posts'),
    path('<int:pk>/create-comment/', CommentCreateApiView.as_view(), name='create_comment'),
    path('<int:pk>/update/', PostUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', PostDeleteAPIView.as_view(), name='delete'),

]