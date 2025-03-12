from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login
from django.db import transaction
from .models import User
from .serializers import UserSerializer, TelegramAuthSerializer, UserProfileSerializer


# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_telegram_user(request):
    telegram_id = request.data.get('telegram_id')
    username = request.data.get('username')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    photo_url = request.data.get('photo_url')

    if not telegram_id:
        return Response({'error': 'telegram_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Проверяем существует ли пользователь с таким telegram_id
        user = User.objects.filter(telegram_id=telegram_id).first()
        
        if not user:
            # Создаем нового пользователя
            user = User.objects.create(
                name=f"{first_name or ''} {last_name or ''}".strip() or f"User_{telegram_id}",
                telegram_id=telegram_id
            )
            
            if photo_url:
                user.avatar = photo_url
            
        # Обновляем данные пользователя если нужно
        if photo_url and not user.avatar:
            user.avatar = photo_url
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TelegramAuthView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        telegram_data = serializer.validated_data
        telegram_id = telegram_data['telegram_id']

        try:
            # Пытаемся найти существующего пользователя
            user = User.objects.get(telegram_id=telegram_id)
            # Обновляем данные пользователя
            if 'username' in telegram_data and telegram_data['username']:
                user.username = telegram_data['username']
            if 'first_name' in telegram_data:
                user.first_name = telegram_data['first_name']
            if 'last_name' in telegram_data:
                user.last_name = telegram_data['last_name']
            if 'photo_url' in telegram_data:
                user.photo_url = telegram_data['photo_url']
            user.save()
        except User.DoesNotExist:
            # Создаем нового пользователя
            user = User.objects.create(
                telegram_id=telegram_id,
                username=telegram_data.get('username', f'user_{telegram_id}'),
                first_name=telegram_data.get('first_name', ''),
                last_name=telegram_data.get('last_name', ''),
                photo_url=telegram_data.get('photo_url'),
            )

        # Авторизуем пользователя
        login(request, user)
        
        return Response({
            'id': user.id,
            'telegram_id': user.telegram_id,
            'username': user.username,
            'is_new': user.date_joined == user.last_login
        })

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

