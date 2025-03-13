from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/telegram/', views.TelegramAuthView.as_view(), name='telegram_auth'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 