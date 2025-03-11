import hashlib
import hmac
import time
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class TelegramAuthentication(authentication.BaseAuthentication):
    """
    Аутентификация пользователя через Telegram.
    """
    def authenticate(self, request):
        # Получаем данные из запроса
        telegram_data = request.data.get('telegram_data', {})
        if not telegram_data:
            return None
        
        # Проверяем обязательные поля
        required_fields = ['id', 'first_name', 'auth_date', 'hash']
        if not all(field in telegram_data for field in required_fields):
            return None
        
        # Проверяем, не истек ли срок действия данных (1 день)
        auth_date = int(telegram_data['auth_date'])
        if time.time() - auth_date > 86400:
            raise AuthenticationFailed('Данные аутентификации устарели')
        
        # Проверяем хэш
        received_hash = telegram_data.pop('hash')
        data_check_string = '\n'.join([f'{key}={value}' for key, value in sorted(telegram_data.items())])
        secret_key = hashlib.sha256(settings.TOKEN.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        if calculated_hash != received_hash:
            raise AuthenticationFailed('Неверный хэш')
        
        # Получаем или создаем пользователя
        try:
            user = User.objects.get(telegram_id=telegram_data['id'])
        except User.DoesNotExist:
            user = User.objects.create(
                telegram_id=telegram_data['id'],
                name=telegram_data.get('first_name', '') + ' ' + telegram_data.get('last_name', ''),
                username=telegram_data.get('username', ''),
            )
        
        return (user, None)

    def authenticate_header(self, request):
        return 'Telegram' 