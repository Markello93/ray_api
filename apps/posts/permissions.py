from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешает доступ к списку или объекту только для чтения.
    Небезопасные запросы доступны только пользователям
    с ролью admin и суперюзерам."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff
