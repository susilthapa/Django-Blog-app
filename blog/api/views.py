from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
from blog.models import Post
from .permissions import IsOwnerOrReadOnly
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__first_name']
    pagination_class = PostPageNumberPagination


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView):             # RetrieveUpdateAPIView show the previous content of updating fields while UpdateAPIView doesnot
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostDetailSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    #
    # def perform_destroy(self, instance):
    #     instance.detele(author=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # lookup_field = 'slug'   # to use slug in url instead of pk






