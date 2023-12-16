from django.urls import include, path
from rest_framework import routers

from api.views import (
    CustomUsersViewSet, CustomLoginView, CustomLogoutView,
    FAQViewset, CustomerVewset
)

router = routers.DefaultRouter()
router.register('users', CustomUsersViewSet)
router.register('faq', FAQViewset)
router.register('customer', CustomerVewset)

auth_patterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', include(auth_patterns)),
]
