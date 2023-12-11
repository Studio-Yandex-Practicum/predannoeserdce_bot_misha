from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from app.models import FAQ, Customer


class CustomLoginSerializer(TokenObtainPairSerializer):
    """
    Сериализатор входа в приложение.
    Модель пользователя модифицирована для входа по email.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data = {'auth_token': data['access']}
        return data


class FAQSerializer(serializers.ModelSerializer):
    """Сериализатор для модели FAQ."""

    class Meta:
        model = FAQ
        fields = ('question', 'answer', 'order')


class CustomerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели клиентов."""

    def validate(self, data):
        """Валидация клиента."""
        # Не допускаем всех пустых полей
        if (
            data.get('email', '') == '' and
            data.get('phone', '') == '' and
            data.get('tg_id', '') == '' and
            data.get('name', '') == ''
        ):
            raise serializers.ValidationError(
                'Хотя бы одно из полей необходимо заполнить.'
            )
        return data

    class Meta:
        model = Customer
        fields = '__all__'
