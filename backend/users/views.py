from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TelegramAuthSerializer, UserProfileSerializer
from django.conf import settings
import hashlib
import hmac
import json
from urllib.parse import parse_qs

class TelegramAuthView(APIView):
    def verify_telegram_data(self, init_data):
        """Проверяет подлинность данных от Telegram"""
        try:
            # Разбираем init_data
            data_dict = dict(parse_qs(init_data))
            data_check_string = '\n'.join([
                f"{k}={v[0]}" for k, v in sorted(data_dict.items()) 
                if k != 'hash'
            ])
            
            # Получаем хеш из данных
            received_hash = data_dict.get('hash', [None])[0]
            if not received_hash:
                return False
            
            # Создаем secret key
            secret_key = hmac.new(
                'WebAppData'.encode(),
                settings.BOT_TOKEN.encode(),
                hashlib.sha256
            ).digest()
            
            # Вычисляем хеш
            calculated_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return calculated_hash == received_hash
        except Exception as e:
            print(f"Error verifying Telegram data: {e}")
            return False

    def post(self, request):
        # Получаем init_data из заголовка
        init_data = request.headers.get('X-Telegram-Init-Data')
        if not init_data or not self.verify_telegram_data(init_data):
            return Response(
                {'error': 'Invalid Telegram data'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TelegramAuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Создаем JWT токены
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            # Добавляем данные пользователя в ответ
            user_data = UserProfileSerializer(user).data
            
            return Response({
                'status': 'success',
                'tokens': tokens,
                'user': user_data
            })
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
