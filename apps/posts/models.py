from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from ray_api.settings import POST_STRING_SIZE

User = get_user_model()


class Post(models.Model):
    """The Post model is used to set parameters for displaying posts on the
    site."""

    CARS = [
        ('bmw', 'bmw'),
        ('mercedes', 'mercedes'),
        ('audi', 'audi'),
        ('porsche', 'porsche'),
        ('nissan', 'nissan'),
        ('mitsubishi', 'mitsubishi'),
    ]
    theme = models.CharField(choices=CARS, max_length=10, null=True)
    text = models.TextField(
        verbose_name='Post text',
    )
    pub_date = models.DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author name',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    image = models.ImageField(
        verbose_name='Post image',
        default='posts/noimage_detail.png',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.text[:POST_STRING_SIZE]


class Comment(models.Model):
    """The Comment model defines the key Post comment options."""

    post = models.ForeignKey(
        Post,
        verbose_name='Linked post',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Author name',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text[:POST_STRING_SIZE]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'post'], name='unique_like')]
