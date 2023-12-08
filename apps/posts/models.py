from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from ray_api.settings import POST_STRING_SIZE

User = get_user_model()


class Post(models.Model):
    """Класс Post используется для задания
    параметров отображения постов на сайте.
    """

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
        verbose_name='Текст поста',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Имя автора',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    image = models.ImageField(
        verbose_name='Изображение коллекции',
        default='posts/noimage_detail.png',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:POST_STRING_SIZE]


class Comment(models.Model):
    """Класс Comment определяет ключевые
    параметры комментариев к постам.
    """

    post = models.ForeignKey(
        Post,
        verbose_name='Ссылка на пост',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Имя автора',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:POST_STRING_SIZE]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'post'], name='unique_like')]


# class PexelsImage(models.Model):
#     url = models.URLField(verbose_name='Ссылка на изображение')
#     description = models.TextField(verbose_name='Описание изображения')
#     photographer = models.CharField(max_length=255, verbose_name='Фотограф')
#
#     def __str__(self):
#         return self.description


# class Like(models.Model):
#     """Класс Follow определяет ключевые
#     параметры системы подписки на авторов.
#     """
#
#     user = models.ForeignKey(
#         User,
#         verbose_name='Имя подписчика',
#         on_delete=models.CASCADE,
#         related_name='follower',
#     )
#     post = models.ForeignKey(
#         Post,
#         verbose_name='Имя автора',
#         on_delete=models.CASCADE,
#         related_name='following',
#     )
#
#     class Meta:
#         UniqueConstraint(name='unique_following', fields=['user', 'post'])
#         verbose_name = 'Подписка'
#         verbose_name_plural = 'Подписки'
