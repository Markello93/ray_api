from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
]