from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
from blog.models import Post


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostListSerializer


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView):             # RetrieveUpdateAPIView show the previous content of
                                                            # updating fields while UpdateAPIView doesnot
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostCreateUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostListSerializer


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # lookup_field = 'slug'   # to use slug in url instead of pk






