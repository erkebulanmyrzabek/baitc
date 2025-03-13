from django.urls import path
from . import views

urlpatterns = [
    path('auth/telegram/', views.telegram_auth, name='telegram-auth'),
    path('profile/', views.user_profile, name='user-profile'),
] 