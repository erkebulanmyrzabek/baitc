from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer, UserProfileSerializer
from .authentication import TelegramAuthentication

class TelegramLoginView(APIView):
    """
    API для входа через Telegram Mini App.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [TelegramAuthentication]
    
    def post(self, request):
        # Аутентификация через Telegram
        user_auth = TelegramAuthentication().authenticate(request)
        if not user_auth:
            return Response({"error": "Ошибка аутентификации"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user, _ = user_auth
        
        # Создаем или получаем токен для пользователя
        token, created = Token.objects.get_or_create(user=user)
        
        # Возвращаем данные пользователя и токен
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })

class TelegramUserProfileView(APIView):
    """
    API для получения и обновления профиля пользователя через Telegram Mini App.
    """
    authentication_classes = [TelegramAuthentication]
    
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TelegramInitDataView(APIView):
    """
    API для проверки и обработки initData из Telegram Mini App.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        init_data = request.data.get('initData', '')
        if not init_data:
            return Response({"error": "Отсутствуют данные инициализации"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Здесь можно добавить проверку initData
        # ...
        
        return Response({"success": True, "message": "Данные инициализации приняты"})

class TelegramWebAppDataView(APIView):
    """
    API для получения данных для Telegram Web App.
    """
    authentication_classes = [TelegramAuthentication]
    
    def get(self, request):
        user = request.user
        
        # Получаем данные для Web App
        hackathons_count = user.hackathon_set.count()
        teams_count = user.community_teams.count()
        
        return Response({
            "user": UserSerializer(user).data,
            "stats": {
                "hackathons_count": hackathons_count,
                "teams_count": teams_count,
                "xp_to_next_level": user.xp_to_next_level(),
                "participation_count": user.participation_count()
            }
        }) 