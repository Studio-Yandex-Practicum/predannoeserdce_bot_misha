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
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'order', 'category')


class CustomerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели клиентов."""

    lookup_field = 'tg_id'

    class Meta:
        model = Customer
        fields = '__all__'
