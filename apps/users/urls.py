from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import UserViewSet

urlpatterns = [
    path(
        '',
        UserViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='user-list-create',
    ),
    path(
        'me/',
        UserViewSet.as_view(
            {'get': 'me', 'put': 'me', 'patch': 'me', 'delete': 'me'}
        ),
    ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
