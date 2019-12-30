from rest_framework.serializers import ModelSerializer

from blog.models import Post


# class PostCreateSerializer(ModelSerializer):
#     class Meta:
#         model = Post
#         fields = [
#             'title',
#             'content',
#             'date_posted',
#             'author',
#         ]

class PostCreateUpdateSerializer(ModelSerializer):  # doesn't allow to update pk/slug
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'date_posted',
        ]


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'date_posted',
            'author',
        ]


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'date_posted',
            'author',
        ]
