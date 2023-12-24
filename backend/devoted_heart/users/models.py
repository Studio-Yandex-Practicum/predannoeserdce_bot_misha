from django.db import models
from django.contrib.auth.models import AbstractUser

from users.validators import UsernameRegexValidator


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        validators=(UsernameRegexValidator(),),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        null=False,
    )
    surname = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        null=False,
    )
    tg_id = models.CharField(
        'ID в Telegram',
        max_length=100,
        blank=True,
        null=True,
    )
    REQUIRED_FIELDS = ('username', )
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.email}'
