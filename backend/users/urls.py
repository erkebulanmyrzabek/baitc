from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TelegramAuthView,
    TokenCheckView,
    CustomTokenRefreshView,
    UserProfileViewSet
)

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/telegram/', TelegramAuthView.as_view(), name='telegram_auth'),
    path('auth/check/', TokenCheckView.as_view(), name='token_check'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
] 