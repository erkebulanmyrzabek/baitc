from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.db.models import F
from .serializers import TelegramAuthSerializer, UserProfileSerializer, AchievementSerializer
from .models import UserProfile, Achievement
from django.conf import settings
import hashlib
import hmac
import json
from urllib.parse import parse_qs
import logging
from django.http import Http404

logger = logging.getLogger(__name__)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.prefetch_related(
            'tech_stack', 'achievements', 'friends', 'hackathons'
        ).all()

    def get_object(self):
        telegram_id = self.request.user.get('telegram_id')
        if not telegram_id:
            raise Http404
        return UserProfile.objects.get(telegram_id=telegram_id)

    @action(detail=True, methods=['post'])
    def add_friend(self, request, pk=None):
        try:
            friend = self.get_object()
            user = UserProfile.objects.get(telegram_id=request.user.get('telegram_id'))
            
            if friend.telegram_id == user.telegram_id:
                return Response(
                    {"error": "Нельзя добавить себя в друзья"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.friends.add(friend)
            return Response({"message": "Друг успешно добавлен"})
        except Exception as e:
            logger.error(f"Error adding friend: {str(e)}")
            return Response(
                {"error": "Ошибка при добавлении друга"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def remove_friend(self, request, pk=None):
        try:
            friend = self.get_object()
            request.user.friends.remove(friend)
            return Response({"message": "Друг успешно удален"})
        except Exception as e:
            logger.error(f"Error removing friend: {str(e)}")
            return Response(
                {"error": "Ошибка при удалении друга"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def friends(self, request, pk=None):
        try:
            user = self.get_object()
            friends = user.friends.all()
            serializer = self.get_serializer(friends, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting friends list: {str(e)}")
            return Response(
                {"error": "Ошибка при получении списка друзей"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def achievements(self, request, pk=None):
        try:
            user = self.get_object()
            achievements = user.achievements.all()
            serializer = AchievementSerializer(achievements, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting achievements list: {str(e)}")
            return Response(
                {"error": "Ошибка при получении списка достижений"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_xp(self, request, pk=None):
        try:
            user = self.get_object()
            amount = request.data.get('amount', 0)
            
            if amount <= 0:
                return Response(
                    {"error": "Количество XP должно быть положительным"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.add_xp(amount)
            return Response({
                "message": f"Добавлено {amount} XP",
                "current_xp": user.xp,
                "current_level": user.level
            })
        except Exception as e:
            logger.error(f"Error adding XP: {str(e)}")
            return Response(
                {"error": "Ошибка при добавлении XP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_crystals(self, request, pk=None):
        try:
            user = self.get_object()
            amount = request.data.get('amount', 0)
            
            if amount <= 0:
                return Response(
                    {"error": "Количество кристаллов должно быть положительным"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.crystals = F('crystals') + amount
            user.save()
            user.refresh_from_db()

            return Response({
                "message": f"Добавлено {amount} кристаллов",
                "current_crystals": user.crystals
            })
        except Exception as e:
            logger.error(f"Error adding crystals: {str(e)}")
            return Response(
                {"error": "Ошибка при добавлении кристаллов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TelegramAuthView(APIView):
    permission_classes = [AllowAny]

    def verify_telegram_data(self, init_data):
        """Проверяет подлинность данных от Telegram"""
        if settings.DEBUG and init_data == 'test_init_data':
            return True

        try:
            data_dict = dict(parse_qs(init_data))
            data_check_string = '\n'.join([
                f"{k}={v[0]}" for k, v in sorted(data_dict.items()) 
                if k != 'hash'
            ])
            
            received_hash = data_dict.get('hash', [None])[0]
            if not received_hash:
                return False
            
            secret_key = hmac.new(
                'WebAppData'.encode(),
                settings.BOT_TOKEN.encode(),
                hashlib.sha256
            ).digest()
            
            calculated_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return calculated_hash == received_hash
        except Exception as e:
            logger.error(f"Error verifying Telegram data: {str(e)}")
            return False

    def post(self, request):
        init_data = request.headers.get('X-Telegram-Init-Data')
        if not init_data or not self.verify_telegram_data(init_data):
            return Response(
                {'error': 'Invalid Telegram data'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TelegramAuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken()
            refresh['telegram_id'] = user.telegram_id
            refresh['type'] = 'refresh'
            
            access = RefreshToken()
            access['telegram_id'] = user.telegram_id
            access['type'] = 'access'
            
            tokens = {
                'refresh': str(refresh),
                'access': str(access),
            }
            
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
            telegram_id = request.user.get('telegram_id')
            if not telegram_id:
                return Response(
                    {"error": "Invalid token"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user = UserProfile.objects.get(telegram_id=telegram_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
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
            if response.status_code == 200:
                telegram_id = request.user.get('telegram_id')
                if telegram_id:
                    user = UserProfile.objects.get(telegram_id=telegram_id)
                    serializer = UserProfileSerializer(user)
                    response.data['user'] = serializer.data
            return response
        except Exception as e:
            logger.error(f"Error in CustomTokenRefreshView: {str(e)}")
            return Response(
                {"error": "Ошибка при обновлении токена"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
