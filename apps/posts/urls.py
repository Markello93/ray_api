from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.posts.views import CommentViewSet, PostViewSet, SearchImageView

v1_router = SimpleRouter()
v1_router.register('', PostViewSet, basename='posts')
v1_router.register('<int:post_id>/comments', CommentViewSet, basename=r'comments')
urlpatterns = [
    path('random_post/', SearchImageView.as_view()),
    path('', include(v1_router.urls)),
]
