from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    CommentCreateView,
                    delete_comment,
                    like_post,
                    )

from .import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('filter-posts/<str:key>/', PostListView.as_view(), name='filter_posts'),
    path('post-comment/<int:pk>/', CommentCreateView.as_view(), name='create-comment'),
    path('delete-comment/', delete_comment, name='delete-comment'),
    path('like-post/', like_post, name='like_post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
]
