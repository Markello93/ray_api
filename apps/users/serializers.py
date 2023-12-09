"""Сериализаторы приложения пользователей."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating user."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'birthday',
            'phone',
            'password',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user CRUD."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff:
            return super().update(instance, validated_data)
        if instance == self.context['request'].user:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        raise serializers.ValidationError(
            'You are not allowed to change this account'
        )

    def destroy(self, instance):
        if self.context['request'].user.is_staff:
            instance.delete()
        if instance == self.context['request'].user:
            instance.delete()
        raise serializers.ValidationError(
            'You do not have the right to delete this account'
        )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'birthday',
            'phone',
            'password',
        )
