import asyncio
import json

import httpx
from adrf.views import APIView
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.posts.models import Like, Post
from apps.posts.serializers import (
    CommentSerializer,
    LikedSerializer,
    PostSerializer,
    RandSerializer,
)


@extend_schema(
    description='Endpoints for managing posts.',
    methods=['get', 'post', 'patch', 'delete'],
)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        cached_posts = cache.get('cached_posts')
        if cached_posts:
            return Response(cached_posts)
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        cache.set('cached_posts', serializer.data, 60 * 60)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        Post.objects.create(
            author=request.user,
            text=request.data.get('text'),
            theme=request.data.get('theme'),
            image=request.data.get('image')
        )
        cache.delete('cached_posts')
        return Response({'message': 'Post created succesfully'},
                        status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete('cached_posts')
        return response

    @extend_schema(
        description='Endpoint for creating likes on a post.',
        methods=['post'],
        request=PostSerializer,
        responses={
            201: {'description': 'Post liked successfully'},
            400: {'description': 'You already rate this post'},
        }
    )
    @extend_schema(
        description='Endpoint for deleting likes on a post.',
        methods=['delete'],
        responses={
            204: {'description': 'Post like removed'},
        }
    )
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def likes(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user,
                                                   post=post)

        if request.method == 'POST':
            if not created:
                return Response({'message': 'You already rate this post'},
                                status=status.HTTP_400_BAD_REQUEST)

            cache.delete(
                f'liked_users_{pk}')
            return Response(status=status.HTTP_201_CREATED)
        cache.delete(f'liked_users_{pk}')
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        description='Endpoint for fetching users who liked a post.',
        methods=['get'],
        responses={
            200: LikedSerializer,
        }
    )
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def liked_by(self, request, pk):
        cached_data = cache.get(f'liked_users_{pk}')
        if cached_data:
            return Response(cached_data)
        post = get_object_or_404(Post, pk=pk)
        liked_users = post.like_set.select_related('user').values_list(
            'user__email', flat=True)
        serializer = LikedSerializer(liked_users, many=True)
        cache.set(f'liked_users_{pk}', liked_users, 60 * 60)
        return Response(serializer.data)


@extend_schema(
    tags=['posts'],
    description='Endpoint for receive post and related pics',
    methods=['post']
)
@method_decorator(csrf_exempt, name='dispatch')
class SearchImageView(APIView):
    serializer_class = RandSerializer

    async def post(self, request):
        theme = json.loads(request.body).get('theme')

        post_task = asyncio.create_task(self.get_post_from_db(theme))
        pics_task = asyncio.create_task(self.get_pics_from_site(theme))

        post, pics = await asyncio.gather(post_task, pics_task)

        serializer_data = {'post': PostSerializer(post).data,
                           'related_photo': pics}

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
                return [pic['src']['original'] for pic in
                        response.json().get('photos')]
            else:
                return None


@extend_schema(
    tags=['comments'],
    description='Endpoints for managing posts.',
    methods=['get', 'post', 'patch', 'delete'],
)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
