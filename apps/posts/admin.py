from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.posts.models import Comment, Like, Post
from ray_api.settings import ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админ модель для товаров магазина."""

    list_display = (
        'pk',
        'text',
        'theme',
        'pub_date',
        'author',
        'price',
        'preview',
    )
    list_editable = ('price',)
    search_fields = (
        'author',
        'price',
        'theme',
    )
    list_filter = (
        'author',
        'price',
        'theme',
    )
    ordering = ('pk',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY

    def preview(self, obj):
        """Отображает картинку в админке."""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100"/>')
        return None

    preview.short_description = 'Изображение'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post', 'text', 'author', 'created']
    search_fields = ['pk', 'post', 'author', 'created']
    ordering = ('post',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
    )
    search_fields = ['user', 'post']
