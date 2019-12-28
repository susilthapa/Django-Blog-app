from rest_framework.generics import ListAPIView

from blog.models import Post


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()