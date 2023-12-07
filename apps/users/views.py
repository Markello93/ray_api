"""Классы представлений для пользователей."""
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet

from apps.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для пользователя магазина."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
