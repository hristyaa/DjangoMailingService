from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    '''Форма для регистрации пользователя'''
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'country', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    """Форма для авторизации (Валидация при блокировке аккаунта)"""
    username = forms.EmailField(label="Email")

    def confirm_login_allowed(self, user):
        if user.is_blocked:
            raise forms.ValidationError(
                "Аккаунт заблокирован.",
                code="blocked"
            )
