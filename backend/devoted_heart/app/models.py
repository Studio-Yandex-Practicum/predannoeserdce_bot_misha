from django.db import models

from core.exceptions import EmptyModelError


class FAQ(models.Model):
    """Часто задаваемый вопрос."""
    question = models.TextField(
        verbose_name='Вопрос',
        help_text='Вопрос',
        unique=True,
        blank=False,
        null=False,
    )
    answer = models.TextField(
        verbose_name='Ответ',
        help_text='Ответ',
        blank=False,
        null=False,
    )
    order = models.SmallIntegerField(
        verbose_name='Порядок вывода',
        help_text='Порядок вывода',
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ('order', )

    def __str__(self) -> str:
        return f'{self.question}'


class Customer(models.Model):
    """Клиент."""
    email = models.EmailField(
        max_length=254,
        verbose_name='Email',
        help_text='Email',
        default='',
    )
    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='Телефон',
        help_text='Телефон',
        default='',
    )
    tg_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='telegram id',
        help_text='telegram id',
        default='',
    )
    name = models.CharField(
        max_length=254,
        verbose_name='Имя',
        help_text='Имя',
        default='',
    )

    def save(self, *args, **kwargs) -> None:
        """Не сохраняем пустую модель."""
        if (
            self.email == '' and self.phone == '' and
            self.tg_id == '' and self.name == ''
        ):
            raise EmptyModelError()
        return super(self).save(*args, **kwargs)

    class Meta:
        ordering = ('id', )

    def __str__(self) -> str:
        return f'Имя: {self.name}'
