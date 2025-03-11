from django.urls import path
from . import views

urlpatterns = [
    path('register-telegram', views.register_telegram_user, name='register-telegram'),
] 