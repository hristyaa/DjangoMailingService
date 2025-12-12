from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name="Аватар", help_text='Загрузите свой аватар')
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True, help_text='Введите номер телефона')
    country = models.CharField(max_length=20, verbose_name='Страна', blank=True, null=True, help_text='Введите свою страну')
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    is_blocked = models.BooleanField(default=False, help_text="Пользователь заблокирован?")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("can_view_users_list", "Может просматривать список пользователей"),
            ("can_block_users", "Может блокировать пользователей"),
            ("can_unblock_users", "Может разблокировать пользователей"),
        ]


    def __str__(self):
        return self.email
