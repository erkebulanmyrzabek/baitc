from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Team, Friendship, Leaderboard, CommunityEvent, UserSearch
from .serializers import (
    TeamSerializer, TeamCreateSerializer, FriendshipSerializer, 
    FriendshipCreateSerializer, LeaderboardSerializer, CommunityEventSerializer,
    CommunityEventCreateSerializer, UserSearchSerializer
)
from user.models import User
from user.serializers import UserSerializer

class TeamViewSet(viewsets.ModelViewSet):
    """
    API для работы с командами.
    """
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        queryset = Team.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeamCreateSerializer
        return TeamSerializer
    
    def perform_create(self, serializer):
        serializer.save(leader=self.request.user)

class JoinTeamView(APIView):
    """
    API для присоединения к команде.
    """
    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        user = request.user
        
        if team.status == 'closed':
            return Response({"error": "Эта команда закрыта для новых участников"}, status=status.HTTP_400_BAD_REQUEST)
        
        if team.is_full:
            return Response({"error": "Команда уже заполнена"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user in team.members.all():
            return Response({"error": "Вы уже в этой команде"}, status=status.HTTP_400_BAD_REQUEST)
        
        team.members.add(user)
        
        return Response({"success": "Вы присоединились к команде"}, status=status.HTTP_200_OK)

class LeaveTeamView(APIView):
    """
    API для выхода из команды.
    """
    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        user = request.user
        
        if user not in team.members.all():
            return Response({"error": "Вы не состоите в этой команде"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user == team.leader:
            return Response({"error": "Лидер не может покинуть команду. Передайте лидерство другому участнику или удалите команду"}, status=status.HTTP_400_BAD_REQUEST)
        
        team.members.remove(user)
        
        return Response({"success": "Вы покинули команду"}, status=status.HTTP_200_OK)

class MyTeamsView(generics.ListAPIView):
    """
    API для просмотра команд пользователя.
    """
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        return self.request.user.community_teams.all()

class FriendshipViewSet(viewsets.ModelViewSet):
    """
    API для работы с запросами на дружбу.
    """
    serializer_class = FriendshipSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(sender=user) | Friendship.objects.filter(receiver=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FriendshipCreateSerializer
        return FriendshipSerializer

class PendingFriendshipsView(generics.ListAPIView):
    """
    API для просмотра ожидающих запросов на дружбу.
    """
    serializer_class = FriendshipSerializer
    
    def get_queryset(self):
        return Friendship.objects.filter(receiver=self.request.user, status='pending')

class AcceptFriendshipView(APIView):
    """
    API для принятия запроса на дружбу.
    """
    def post(self, request, friendship_id):
        friendship = get_object_or_404(Friendship, id=friendship_id, receiver=request.user, status='pending')
        
        friendship.status = 'accepted'
        friendship.save()
        
        # Добавляем пользователей в друзья друг к другу
        friendship.sender.friends.add(friendship.receiver)
        friendship.receiver.friends.add(friendship.sender)
        
        return Response({"success": "Запрос на дружбу принят"}, status=status.HTTP_200_OK)

class RejectFriendshipView(APIView):
    """
    API для отклонения запроса на дружбу.
    """
    def post(self, request, friendship_id):
        friendship = get_object_or_404(Friendship, id=friendship_id, receiver=request.user, status='pending')
        
        friendship.status = 'rejected'
        friendship.save()
        
        return Response({"success": "Запрос на дружбу отклонен"}, status=status.HTTP_200_OK)

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра лидерборда.
    """
    serializer_class = LeaderboardSerializer
    
    def get_queryset(self):
        queryset = Leaderboard.objects.all()
        period = self.request.query_params.get('period', 'all_time')
        queryset = queryset.filter(period=period)
        return queryset.order_by('rank')

class CommunityEventViewSet(viewsets.ModelViewSet):
    """
    API для работы с событиями сообщества.
    """
    serializer_class = CommunityEventSerializer
    
    def get_queryset(self):
        queryset = CommunityEvent.objects.all()
        event_type = self.request.query_params.get('event_type', None)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommunityEventCreateSerializer
        return CommunityEventSerializer
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class RegisterForEventView(APIView):
    """
    API для регистрации на событие.
    """
    def post(self, request, event_id):
        event = get_object_or_404(CommunityEvent, id=event_id)
        user = request.user
        
        if event.is_past:
            return Response({"error": "Это событие уже завершилось"}, status=status.HTTP_400_BAD_REQUEST)
        
        if event.is_full:
            return Response({"error": "Регистрация на это событие закрыта, достигнуто максимальное количество участников"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user in event.participants.all():
            return Response({"error": "Вы уже зарегистрированы на это событие"}, status=status.HTTP_400_BAD_REQUEST)
        
        event.participants.add(user)
        
        return Response({"success": "Вы успешно зарегистрировались на событие"}, status=status.HTTP_200_OK)

class UnregisterFromEventView(APIView):
    """
    API для отмены регистрации на событие.
    """
    def post(self, request, event_id):
        event = get_object_or_404(CommunityEvent, id=event_id)
        user = request.user
        
        if event.is_past:
            return Response({"error": "Это событие уже завершилось"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user not in event.participants.all():
            return Response({"error": "Вы не зарегистрированы на это событие"}, status=status.HTTP_400_BAD_REQUEST)
        
        event.participants.remove(user)
        
        return Response({"success": "Вы отменили регистрацию на событие"}, status=status.HTTP_200_OK)

class UserSearchView(APIView):
    """
    API для поиска пользователей.
    """
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({"error": "Необходимо указать параметр поиска q"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Сохраняем запрос в историю поиска
        UserSearch.objects.create(user=request.user, query=query)
        
        # Ищем пользователей по имени
        users = User.objects.filter(name__icontains=query)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
