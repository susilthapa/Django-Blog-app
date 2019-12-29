from rest_framework.generics import ListAPIView
from .serializers import PostSerializer
from blog.models import Post


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
