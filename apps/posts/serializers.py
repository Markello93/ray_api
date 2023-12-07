"""Сериализаторы для приложения product."""
from rest_framework import serializers

from apps.posts.models import Comment, Like, Post


class LikeSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Like."""

    class Meta:
        model = Like
        fields = (
            'user',
            'post',
        )


class PostSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    price = serializers.IntegerField()
    id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'pub_date',
            'author',
            'image',
            'price',
        )
        read_only_fields = fields


class RandSerializer(serializers.Serializer):
    post = PostSerializer()
    related_photo = serializers.ListField(child=serializers.URLField())


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'created')
        model = Comment
        read_only_fields = ('post',)
