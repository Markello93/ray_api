from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import EmailField

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {'email': EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for creating user in admin panel.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ('email',)
        field_classes = {'email': EmailField}
        error_messages = {'email': {'unique': 'This email address is already '
                                              'taken.'}}
