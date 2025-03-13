from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import TelegramAuthSerializer, UserProfileSerializer
from django.conf import settings
import hashlib
import hmac
import json
from urllib.parse import parse_qs
import logging

logger = logging.getLogger(__name__)

class TelegramAuthView(APIView):
    permission_classes = [AllowAny]

    def verify_telegram_data(self, init_data):
        """Проверяет подлинность данных от Telegram"""
        # В режиме разработки пропускаем проверку
        if settings.DEBUG and init_data == 'test_init_data':
            return True

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

class TokenCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if not hasattr(user, 'telegram_id'):
                return Response(
                    {"error": "Invalid user object"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in TokenCheckView: {str(e)}")
            return Response(
                {"error": "Ошибка при проверке токена"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200 and hasattr(request, 'user'):
                user = request.user
                if hasattr(user, 'telegram_id'):
                    serializer = UserProfileSerializer(user)
                    response.data['user'] = serializer.data
            return response
        except Exception as e:
            logger.error(f"Error in CustomTokenRefreshView: {str(e)}")
            return Response(
                {"error": "Ошибка при обновлении токена"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
