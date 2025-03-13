from django.urls import path
from .views import TelegramAuthView, TokenCheckView, CustomTokenRefreshView

urlpatterns = [
    path('auth/telegram/', TelegramAuthView.as_view(), name='telegram_auth'),
    path('auth/check/', TokenCheckView.as_view(), name='token_check'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
] 