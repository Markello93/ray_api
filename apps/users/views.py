"""Классы представлений для пользователей."""
from django.contrib.auth import get_user_model

# from djoser.serializers import UserCreateSerializer
from django.http import Http404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.users.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model, allow changing user profile, and create/delete
    users."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    lookup_field = 'email'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email',)

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'list':
            return [IsAdminUser()]
        return []

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(['get', 'put', 'patch', 'delete'], detail=False, url_path='me')
    def me(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {'message': 'You must register to view your profile.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user = request.user
        try:
            if request.method == 'GET':
                serializer = self.get_serializer(instance=user)
                return Response(serializer.data)
            elif request.method in ['PUT', 'PATCH']:
                serializer = self.get_serializer(
                    user, data=request.data, partial=True
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(
                        {'message': 'Profile updated successfully'},
                        status=status.HTTP_200_OK,
                    )
            elif request.method == 'DELETE':
                user.delete()
                return Response(
                    {'message': 'User account deleted successfully'},
                    status=status.HTTP_204_NO_CONTENT,
                )
        except User.DoesNotExist:
            raise NotFound({'message': 'User account not found'})
        except Exception as err:
            raise ValidationError({'message': str(err)})
        raise Http404
