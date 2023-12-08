import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from apps.posts.models import Comment, Post, User
from apps.posts.views import PostViewSet


class TestPostViewSet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PostViewSet.as_view({'get': 'list', 'post': 'create'})
        self.user = User.objects.create(email='test@example.com',
                                        password='testpassword')
        self.post_data = {
            'text': 'Test post',
            'theme': 'Test theme',
        }

    def test_list_posts(self):
        request = self.factory.get('/posts/')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        request = self.factory.post('/posts/', self.post_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_post(self):
        post = Post.objects.create(author=self.user, text='Test post',
                                   theme='Test theme')
        view = PostViewSet.as_view({'post': 'likes'})
        request = self.factory.post(f'/posts/{post.id}/likes/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=post.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unlike_post(self):
        post = Post.objects.create(author=self.user, text='Test post',
                                   theme='Test theme')
        post.like_set.create(user=self.user)
        view = PostViewSet.as_view({'delete': 'likes'})
        request = self.factory.delete(f'/posts/{post.id}/likes/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=post.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_liked_by(self):
        post = Post.objects.create(author=self.user, text='Test post',
                                   theme='Test theme')
        post.like_set.create(user=self.user)
        view = PostViewSet.as_view({'get': 'liked_by'})
        request = self.factory.get(f'/posts/{post.id}/liked_by/')
        response = view(request, pk=post.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        post = Post.objects.create(author=self.user, text='Test post',
                                   theme='Test theme')
        view = PostViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'/posts/{post.id}/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=post.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test_user',
                                             password='test_password')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user, text='Test post')

    def test_create_comment_success(self):
        url = reverse('comments-list', kwargs={'post_id': self.post.pk})
        data = {'text': 'Test comment'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.text, 'Test comment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_create_comment_without_text(self):
        url = reverse('comments-list', kwargs={'post_id': self.post.pk})
        data = {}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    def test_list_comments(self):
        comment1 = Comment.objects.create(author=self.user, post=self.post,
                                          text='Comment 1')
        comment2 = Comment.objects.create(author=self.user, post=self.post,
                                          text='Comment 2')
        url = reverse('comments-list', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['text'], comment2.text)
        self.assertEqual(data[1]['text'], comment1.text)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        url = reverse('comments-list', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
