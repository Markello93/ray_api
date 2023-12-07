"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from apps.posts.views import CommentViewSet, PostViewSet, SearchImageView

v1_router = SimpleRouter()
v1_router.register('posts', PostViewSet, basename='posts')
# v1_router.register('comments', CommentViewSet, basename='comments')
# v1_router.register(
#     r'posts/<int:post_id>/comments/',
#     CommentViewSet,
#     basename=r'comments',
# )

v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename=r'comments'
)
# v1_router.register('random_post', get_random_post, basename='random_post')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/auth/', include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('auth/', include('djoser.urls')),
    path('random_post/', SearchImageView.as_view(), name='random_post'),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
    path('', include(v1_router.urls))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
