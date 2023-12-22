from django.db import models


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
        verbose_name = 'ЧаВо'
        verbose_name_plural = 'ЧаВо'

    def __str__(self) -> str:
        return f'{self.question}'


class Customer(models.Model):
    """Клиент."""
    email = models.EmailField(
        max_length=254,
        verbose_name='Email',
        help_text='Email',
        unique=True,
        blank=False,
        null=False,
    )
    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='Телефон',
        help_text='Телефон',
        blank=False,
        null=False,
    )
    tg_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='telegram id',
        help_text='telegram id',
        blank=False,
        null=False,
    )
    name = models.CharField(
        max_length=254,
        verbose_name='Имя',
        help_text='Имя',
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ('id', )
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиент'

    def __str__(self) -> str:
        return f'Имя: {self.name}'
