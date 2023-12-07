from django.contrib.auth.models import UserManager as DjangoUserManager
from django.utils.crypto import get_random_string


class UserManager(DjangoUserManager):
    """Индивидуальная модель пользователя."""

    def _create_user(self, email: str, password: str | None, **extra_fields):
        """Creating user with email."""

        if not email:
            raise ValueError("Необходим email.")
        if password is None:
            password = get_random_string(length=12)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str | None = None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields
    ):
        """Creating superuser with email."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)