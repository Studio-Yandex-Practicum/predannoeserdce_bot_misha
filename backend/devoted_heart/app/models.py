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


class Messages(models.Model):
    """Сообщения"""
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE,
        null=True, blank=True
    )
    text = models.TextField(
        max_length=4096,
        null=True,
        blank=True,
        verbose_name='Текст сообщения от администратора',
    )
    image = models.ImageField(
        upload_to='message_images/',
        null=True,
        blank=True,
        verbose_name='Фотография',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    selected = models.BooleanField(
        default=False,
        verbose_name='Дополнить планировщик сообщением от администратора',
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"{self.customer} - {self.timestamp}"
