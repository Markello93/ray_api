from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Comment, Post


@receiver(post_save, sender=Comment)
def invalidate_comment_cache(sender, instance, created, **kwargs):
    if created:
        cache.delete(f'comments_for_post_{instance.post.id}')


@receiver(post_delete, sender=Comment)
def invalidate_comment_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f'comments_for_post_{instance.post.id}')


@receiver(post_save, sender=Post)
def invalidate_comment_cache_on_post_update(sender, instance, created, **kwargs):
    if not created:
        cache.delete(f'comments_for_post_{instance.id}')


@receiver(post_delete, sender=Post)
def invalidate_post_cache_on_delete(sender, instance, **kwargs):
    cache.delete('cached_posts')
