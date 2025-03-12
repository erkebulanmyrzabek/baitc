from django.urls import path
from .views import TelegramAuthView, UserProfileView

urlpatterns = [
    path('auth/telegram/', TelegramAuthView.as_view(), name='telegram-auth'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
] 