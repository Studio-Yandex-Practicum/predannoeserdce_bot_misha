from django.urls import include, path
from rest_framework import routers

from api.views import (
    CustomUsersViewSet, CustomLoginView, CustomLogoutView,
    FAQViewset, CustomerVewset
)
from core.constants import ApiEnabled

router = routers.DefaultRouter()

if ApiEnabled.ENABLE_USERS:
    router.register('users', CustomUsersViewSet)
if ApiEnabled.ENABLE_FAQ:
    router.register('faq', FAQViewset)
if ApiEnabled.ENABLE_CUSTOMER:
    router.register('customer', CustomerVewset)

auth_patterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', include(auth_patterns)),
]
