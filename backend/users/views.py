from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer

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
        # Проверяем существует ли профиль с таким telegram_id
        profile = UserProfile.objects.filter(telegram_id=telegram_id).first()
        
        if not profile:
            # Создаем нового пользователя Django
            user = User.objects.create_user(
                username=username or f"tg_{telegram_id}",
                first_name=first_name or "",
                last_name=last_name or ""
            )
            
            # Создаем профиль пользователя
            profile = UserProfile.objects.create(
                user=user,
                telegram_id=telegram_id
            )

        # Обновляем данные профиля
        if photo_url:
            profile.photo = photo_url
        profile.save()

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
