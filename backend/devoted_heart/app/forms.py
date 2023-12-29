from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator, FileExtensionValidator,
)
from sys import getsizeof

from .models import Messages
from core.constants import LIMIT_VALUE_TEXT

LIMIT_VALUE_IMAGE = 1 * 1024 * 1024  # 1MB
FILE_EXTENSION_LIST = ['jpg', 'jpeg', 'png']
MESSAGE_TEXT = 'Длинное сообщение'
MESSAGE_IMAGE_EXT = 'Неправильный тип файла'
MESSAGE_IMAGE_SIZE = 'Размер изображения не должен превышать 1MB.'


def validate_image_size(value):
    """Максимальный размер изображения (в байтах)"""
    max_size = LIMIT_VALUE_IMAGE

    if value:
        image_size = getsizeof(value.read())
        if image_size > max_size:
            raise ValidationError()


class MessagesForm(forms.ModelForm):
    text = forms.CharField(
        validators=[
            MaxLengthValidator(
                limit_value=LIMIT_VALUE_TEXT,
                message=MESSAGE_TEXT
            ),
        ],
        required=False
    )
    image = forms.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=FILE_EXTENSION_LIST,
                message=MESSAGE_IMAGE_EXT
            ),
            validate_image_size,

        ],
        required=False
    )

    class Meta:
        model = Messages
        fields = ('text', 'image', 'selected')
