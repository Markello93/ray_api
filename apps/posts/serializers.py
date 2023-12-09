from rest_framework import serializers

from apps.posts.models import Comment, Like, Post


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for the Like model."""

    class Meta:
        model = Like
        fields = (
            'user',
            'post',
        )


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'theme',
            'pub_date',
            'author',
            'image',
        )
        read_only_fields = ('id', 'pub_date', 'author')


class RandSerializer(serializers.Serializer):
    post = PostSerializer()
    related_photo = serializers.ListField(child=serializers.URLField())


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'created')
        model = Comment
        read_only_fields = ('post',)


class LikedSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.EmailField()
    )
