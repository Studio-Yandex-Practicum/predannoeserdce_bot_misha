from django.db import models


class Category(models.Model):
    """Категории вопросов."""
    name = models.CharField(
        verbose_name='Категория',
        help_text='Категория',
        blank=False,
        null=False,
        unique=True,
        max_length=100,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return f'{self.name}'


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
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория',
        on_delete=models.CASCADE,
        related_name='questions',
    )

    class Meta:
        ordering = ('order',)
        verbose_name = 'Часто задаваемые вопросы'
        verbose_name_plural = 'Часто задаваемые вопросы'

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
    registration_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
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
        verbose_name = "Сообщение"
        verbose_name_plural = 'Сообщения'
        ordering = ('id',)

    def __str__(self):
        return f"{self.customer} - {self.timestamp}"
