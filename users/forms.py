from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    '''Форма для регистрации пользователя'''
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'country', 'password1', 'password2')
