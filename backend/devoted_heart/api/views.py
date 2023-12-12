from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.views import TokenDestroyView, UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, viewsets

from api.serializer import (
    CustomLoginSerializer, FAQSerializer, CustomerSerializer
)
from app.models import FAQ, Customer


class CustomLoginView(TokenObtainPairView):
    """View класс входа в приложение."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomLoginSerializer


class CustomLogoutView(TokenDestroyView):
    """View класс выхода из приложения."""
    permission_classes = (permissions.IsAuthenticated,)


class CustomUsersViewSet(UserViewSet):
    """View-crud класс для пользователя(ей)."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    search_fields = ('username', 'tg_id')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    http_method_names = ('get',)


class FAQViewset(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    """View-read класс для FAQ."""
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = (permissions.AllowAny,)


class CustomerVewset(viewsets.ModelViewSet):
    """View-crud класс для клиентов."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'tg_id'
