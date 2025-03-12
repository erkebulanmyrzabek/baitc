from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

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

