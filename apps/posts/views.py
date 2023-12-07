import asyncio
import json

import httpx
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from apps.posts.models import Post
from apps.posts.permissions import IsOwnerOrAdmin
from apps.posts.serializers import CommentSerializer, PostSerializer, RandSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для товаров."""

    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SearchImageView(View):
    async def post(self, request):
        theme = json.loads(request.body).get('theme')

        post_task = asyncio.create_task(self.get_post_from_db(theme))
        pics_task = asyncio.create_task(self.get_pics_from_site(theme))

        post, pics = await asyncio.gather(post_task, pics_task)

        serializer_data = {'post': PostSerializer(post).data, 'related_photo': pics}

        serializer = RandSerializer(data=serializer_data)
        if serializer.is_valid():
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)

    async def get_post_from_db(self, car_type):
        post = await Post.objects.filter(theme=car_type).alast()
        return post

    async def get_pics_from_site(self, car_type):
        url = 'https://api.pexels.com/v1/search'
        params = {'query': car_type, 'page': '1', 'per_page': '10'}
        headers = {
            'Authorization': 'jgkXduK1KgvFLzVMyC99qzdMsuKq6VFAeOhAZqhZVh3PYx0ZTbMOUFV0'
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            if response.status_code == 200:
                return [pic['src']['original'] for pic in response.json().get('photos')]
            else:
                return None


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
