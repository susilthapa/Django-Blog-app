from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    StringRelatedField,
)
from rest_framework import serializers 
from blog.models import Post, Comment
from users.api.serializers import UserDetailSerializer


class CommentListSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    post = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'author',
            'post',
            'text',
            'created_date'
        ]
        extra_kwargs ={'created_date':{'read_only':'True'}}


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='detail',
        # lookup_field='pk'  ( pk is default lookup field if slug field is used it should be mentioned here )
    )
    # profile_url = HyperlinkedIdentityField(
    #     view_name='api-profile',
    #     lookup_field='pk'
    # )

    # author = UserDetailSerializer(read_only=True)
    author = StringRelatedField()
    # author = HyperlinkedIdentityField(
    #     view_name='user_posts', lookup_field='pk')
    comments = CommentListSerializer(many=True)

    class Meta:
        model = Post
        fields = [  # fields to serialize
            'url',
            'author',
            # 'profile_url',
            'id',
            'title',
            'short_description',
            'comments',
            'total_likes',
            'date_posted',
        ]
        extra_kwargs = {'date_posted':{'read_only':True}}
    # def get_author(self, obj):
    #     return obj.author.username

# def required(value):
#     if value is None:
#         return serializers.ValidationError('This fieldis required')

class PostCreateUpdateSerializer(ModelSerializer):  # doesn't allow to update pk/slug
    # title = serializers.CharField(validators=[required])
    url = HyperlinkedIdentityField(
        view_name='detail',)
    author = StringRelatedField()

    class Meta:
        model = Post
        fields = [
            'url',
            'author',
            'title',
            'content',
            # 'date_posted',
        ]


class PostDetailSerializer(ModelSerializer):
    delete_url = HyperlinkedIdentityField(
        view_name='delete',
        lookup_field='pk'
    )
    comments = CommentListSerializer(many=True)
    author = UserDetailSerializer(read_only=True)
    image = SerializerMethodField(read_only=True)
    # html = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'author',
            'image',
            'title',
            'content',
            'comments',
            'total_likes',
            'date_posted',
            'delete_url',
        ]

        extra_kwargs = {'date_posted':{'read_only':True}}

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


