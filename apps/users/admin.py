from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from apps.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name', 'birthday')}),
        (
            'Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')},
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ['email', 'first_name', 'last_name', 'birthday']
    search_fields = ['email', 'last_name']
    list_filter = ['is_superuser']
    ordering = ('-date_joined',)
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
