from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from blog.models import Post
from users.api.serializers import UserDetailSerializer


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
            'url',
            'title',
            'content',
            'date_posted',
        ]


class PostDetailSerializer(ModelSerializer):
    delete_url = HyperlinkedIdentityField(
        view_name='delete',
        lookup_field='pk'
    )
    author = UserDetailSerializer
    image = SerializerMethodField(read_only=True)
    # html = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'author',
            'image',
            'title',
            'content',
            'date_posted',
            'delete_url',
        ]

    # def get_author(self, obj):
    #     return obj.author.username

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    # def get_html(self, obj):
    #     return obj.get_markdown() # doesnot have this method in Post


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='detail',
        # lookup_field='pk'  ( pk is default lookup field if slug field is used it should be mentioned here )
    )
    author = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [  # fields to serialize
            'url',
            'author',
            'id',
            'title',
            'content',
            'date_posted',
        ]

    # def get_author(self, obj):
    #     return obj.author.username
