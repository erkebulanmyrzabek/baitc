from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import User, Skill, Achievement, Certificate, UserNotification
from .serializers import (
    UserSerializer, SkillSerializer, AchievementSerializer, 
    CertificateSerializer, UserNotificationSerializer,
    UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer
)

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API для работы с пользователями.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра навыков.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
    def get_queryset(self):
        queryset = Skill.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра достижений.
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра сертификатов.
    """
    serializer_class = CertificateSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return Certificate.objects.filter(user_id=user_id)
        return Certificate.objects.all()

class UserNotificationViewSet(viewsets.ModelViewSet):
    """
    API для работы с уведомлениями пользователя.
    """
    serializer_class = UserNotificationSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return UserNotification.objects.filter(user_id=user_id)
        return UserNotification.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UserRegistrationView(generics.CreateAPIView):
    """
    API для регистрации пользователя.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    """
    API для входа пользователя.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API для просмотра и обновления профиля пользователя.
    """
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user

class FriendsListView(generics.ListAPIView):
    """
    API для просмотра списка друзей.
    """
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return self.request.user.friends.all()

class AddFriendView(APIView):
    """
    API для добавления друга.
    """
    def post(self, request, hash_code):
        friend = get_object_or_404(User, hash_code=hash_code)
        user = request.user
        
        if friend == user:
            return Response({"error": "Вы не можете добавить себя в друзья"}, status=status.HTTP_400_BAD_REQUEST)
        
        if friend in user.friends.all():
            return Response({"error": "Этот пользователь уже в вашем списке друзей"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.friends.add(friend)
        friend.friends.add(user)
        
        return Response({"success": "Пользователь добавлен в друзья"}, status=status.HTTP_200_OK)

class RemoveFriendView(APIView):
    """
    API для удаления друга.
    """
    def post(self, request, hash_code):
        friend = get_object_or_404(User, hash_code=hash_code)
        user = request.user
        
        if friend not in user.friends.all():
            return Response({"error": "Этот пользователь не в вашем списке друзей"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.friends.remove(friend)
        friend.friends.remove(user)
        
        return Response({"success": "Пользователь удален из друзей"}, status=status.HTTP_200_OK)

class UnlockAchievementView(APIView):
    """
    API для разблокировки достижения.
    """
    def post(self, request, achievement_id):
        achievement = get_object_or_404(Achievement, id=achievement_id)
        user = request.user
        
        if achievement in user.achievements.all():
            return Response({"error": "Это достижение уже разблокировано"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.add_achievement(achievement)
        
        return Response({
            "success": "Достижение разблокировано",
            "xp_reward": achievement.xp_reward,
            "crystal_reward": achievement.crystal_reward
        }, status=status.HTTP_200_OK)
