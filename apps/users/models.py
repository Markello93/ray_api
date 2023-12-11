"""Модели приложения users."""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import CharField, DateField, EmailField
from django.utils import timezone

from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    email = EmailField('Email', unique=True)
    phone = CharField('Phone', max_length=30, blank=True, null=True)
    first_name = CharField('Name', max_length=30, blank=True, null=True)
    last_name = CharField('Surname', max_length=50, blank=True, null=True)
    birthday = DateField('Birthday', blank=True, null=True)
    date_joined = models.DateTimeField('Creating date', default=timezone.now)
    is_staff = models.BooleanField('User status', default=False)
    is_active = models.BooleanField('Active', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Returns first_name and last_name."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Returns first_name."""
        return self.first_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
