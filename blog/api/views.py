from django.shortcuts import get_object_or_404
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
    permission_classes = [AllowAny]


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAuthenticated] # cause IsAuthenticatedOrReadOnly is made default permission in setting

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView):             # RetrieveUpdateAPIView show the previous content of updating fields while UpdateAPIView doesnot
    queryset = Post.objects.all().order_by('-date_posted')
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostCreateUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # def perform_destroy(self, instance):
    #     instance.delete()


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    # lookup_field = 'slug'   # to use slug in url instead of pk






