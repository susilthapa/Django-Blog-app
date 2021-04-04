from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

# from rest_framework.filters import (
#     SearchFilter,
#     OrderingFilter,
# )

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
import json
from django.core import serializers
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer, CommentListSerializer
from blog.models import Post, Comment
from users.models import User
from .permissions import IsOwnerOrReadOnly
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

# class PostListAPIView(generics.ListCreateAPIView):
#     queryset = Post.objects.all().order_by('-date_posted')
#     serializer_class = PostListSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ['title', 'content', 'author__username']
#     pagination_class = PostPageNumberPagination
#     # permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    # filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__first_name']
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAuthenticated]

    # def get_queryset(self, *args, **kwargs):
    #     queryset_list = Post.objects.all()
    #     username = self.request.GET.get('username')
    #     # print(username)
    #     if username:
    #         queryset_list = queryset_list.filter(author__username__icontains=username)
    #         return queryset_list
    #     return queryset_list


# class UserPostListApiView(ListAPIView):
#     serializer_class = PostListSerializer
#     pagination_class = PostPageNumberPagination

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated] # cause IsAuthenticatedOrReadOnly is made default permission in setting

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



# class PostUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all().order_by('-date_posted')
#     permission_classes = [IsOwnerOrReadOnly]
#     serializer_class = PostDetailSerializer

#     def perform_update(self, serializer):
#         serializer.save(author=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    # permission_classes = [IsAuthenticated]
    # lookup_field = 'pk'   # to use slug in url instead of pk


class PostUpdateAPIView(RetrieveUpdateAPIView):  # RetrieveUpdateAPIView show the previous content of updating fields while UpdateAPIView doesnot
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostDetailSerializer

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # def perform_destroy(self, instance):
    #     instance.delete()

class PostLikeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        id = data['id']
        key = data['key']
        print(f'Liked = {id}')
        post = get_object_or_404(Post, id=id)
        print(post)
        # serializer = PostDetailSerializer(data=post)
        # if serializer.is_valid():
        # #     print(serializer.data)
        if key =='like':
            post.likes.add(request.user)
        elif key == 'dislike':
            post.likes.remove(request.user)
        # post.save()
        data = {
            # 'post': serializers.serialize('json', post),
            'total_likes': post.total_likes
            }
        return Response(json.dumps(data), status=status.HTTP_200_OK)


class CommentCreateApiView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentListSerializer

    def perform_create(self, serializer):
        # data = json.loads(self.request.data)
        # print(serializer.data)
        # print(self.request.query_params.get('pk'))
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)








