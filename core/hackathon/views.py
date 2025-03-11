from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Hackathon, Tag, PrizePlaces, Track, Team, Solution, SolutionReview, FAQ, LiveStream
from user.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    HackathonSerializer, TagSerializer, PrizePlacesSerializer, TrackSerializer,
    TeamSerializer, TeamCreateSerializer, SolutionSerializer, SolutionCreateSerializer,
    SolutionReviewSerializer, SolutionReviewCreateSerializer, FAQSerializer,
    LiveStreamSerializer, HackathonCreateSerializer
)

# Create your views here.
def hackathon_list(request):
    # Получаем хэш из параметров запроса
    hash_code = request.GET.get("hash")
    user = get_object_or_404(User, hash_code=hash_code) if hash_code else None

    # Получаем все хакатоны
    hackathons = Hackathon.objects.all().order_by('-start_hackathon')

    # Фильтрация по статусу
    status = request.GET.get('status', 'all')
    now = timezone.now()

    if status == 'registration':
        hackathons = hackathons.filter(
            start_registration__lte=now,
            end_registration__gte=now
        )
    elif status == 'active':
        hackathons = hackathons.filter(
            start_hackathon__lte=now,
            end_hackathon__gte=now
        )
    elif status == 'finished':
        hackathons = hackathons.filter(
            end_hackathon__lt=now
        )
    elif status == 'upcoming':
        hackathons = hackathons.filter(
            start_hackathon__gt=now
        )

    # Поиск по названию или описанию
    search_query = request.GET.get('search', '')
    if search_query:
        hackathons = hackathons.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Пагинация
    paginator = Paginator(hackathons, 12)  # 12 хакатонов на страницу
    page = request.GET.get('page', 1)
    hackathons = paginator.get_page(page)

    context = {
        'user': user,
        'hackathons': hackathons,
        'current_status': status,
        'current_search': search_query,
    }

    return render(request, 'hackathon/hackathon_list.html', context)

def hackathon_detail(request, pk):
    user = None
    if 'hash' in request.GET:
        user = get_object_or_404(User, hash_code=request.GET.get('hash'))
    
    hackathon = get_object_or_404(Hackathon, pk=pk)
    
    context = {
        'hackathon': hackathon,
        'user': user,
    }
    
    return render(request, 'hackathon/hackathon_detail.html', context)

# API views
class HackathonViewSet(viewsets.ModelViewSet):
    """
    API для работы с хакатонами.
    """
    serializer_class = HackathonSerializer
    
    def get_permissions(self):
        """
        Разрешения:
        - Для просмотра списка и деталей хакатонов аутентификация не требуется
        - Для создания, обновления и удаления требуется аутентификация
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Hackathon.objects.all()
        status = self.request.query_params.get('status', None)
        type = self.request.query_params.get('type', None)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if type:
            queryset = queryset.filter(type=type)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return HackathonCreateSerializer
        return HackathonSerializer
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class TagViewSet(viewsets.ModelViewSet):
    """
    API для работы с тегами.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PrizePlacesViewSet(viewsets.ModelViewSet):
    """
    API для работы с призовыми местами.
    """
    queryset = PrizePlaces.objects.all()
    serializer_class = PrizePlacesSerializer

class TrackViewSet(viewsets.ModelViewSet):
    """
    API для работы с треками хакатонов.
    """
    serializer_class = TrackSerializer
    
    def get_queryset(self):
        queryset = Track.objects.all()
        hackathon_id = self.request.query_params.get('hackathon_id', None)
        
        if hackathon_id:
            queryset = queryset.filter(hackathon_id=hackathon_id)
        
        return queryset

class TeamViewSet(viewsets.ModelViewSet):
    """
    API для работы с командами.
    """
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        queryset = Team.objects.all()
        hackathon_id = self.request.query_params.get('hackathon_id', None)
        track_id = self.request.query_params.get('track_id', None)
        status = self.request.query_params.get('status', None)
        
        if hackathon_id:
            queryset = queryset.filter(hackathon_id=hackathon_id)
        
        if track_id:
            queryset = queryset.filter(track_id=track_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeamCreateSerializer
        return TeamSerializer
    
    def perform_create(self, serializer):
        serializer.save(leader=self.request.user)

class SolutionViewSet(viewsets.ModelViewSet):
    """
    API для работы с решениями.
    """
    serializer_class = SolutionSerializer
    
    def get_queryset(self):
        queryset = Solution.objects.all()
        hackathon_id = self.request.query_params.get('hackathon_id', None)
        track_id = self.request.query_params.get('track_id', None)
        team_id = self.request.query_params.get('team_id', None)
        status = self.request.query_params.get('status', None)
        
        if hackathon_id:
            queryset = queryset.filter(hackathon_id=hackathon_id)
        
        if track_id:
            queryset = queryset.filter(track_id=track_id)
        
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SolutionCreateSerializer
        return SolutionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SolutionReviewViewSet(viewsets.ModelViewSet):
    """
    API для работы с отзывами на решения.
    """
    serializer_class = SolutionReviewSerializer
    
    def get_queryset(self):
        queryset = SolutionReview.objects.all()
        solution_id = self.request.query_params.get('solution_id', None)
        
        if solution_id:
            queryset = queryset.filter(solution_id=solution_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SolutionReviewCreateSerializer
        return SolutionReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class FAQViewSet(viewsets.ModelViewSet):
    """
    API для работы с FAQ.
    """
    serializer_class = FAQSerializer
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        hackathon_id = self.request.query_params.get('hackathon_id', None)
        
        if hackathon_id:
            queryset = queryset.filter(hackathon_id=hackathon_id)
        
        return queryset

class LiveStreamViewSet(viewsets.ModelViewSet):
    """
    API для работы с прямыми трансляциями.
    """
    serializer_class = LiveStreamSerializer
    
    def get_queryset(self):
        queryset = LiveStream.objects.all()
        hackathon_id = self.request.query_params.get('hackathon_id', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if hackathon_id:
            queryset = queryset.filter(hackathon_id=hackathon_id)
        
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')
        
        return queryset

class RegisterForHackathonView(APIView):
    """
    API для регистрации на хакатон.
    """
    def post(self, request, hackathon_id):
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        user = request.user
        
        # Проверяем, открыта ли регистрация
        now = timezone.now().date()
        if now < hackathon.start_registation or now > hackathon.end_registration:
            return Response({"error": "Регистрация на этот хакатон закрыта"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, не зарегистрирован ли уже пользователь
        if hackathon.solo_participants.filter(id=user.id).exists():
            return Response({"error": "Вы уже зарегистрированы на этот хакатон"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Регистрируем пользователя
        hackathon.solo_participants.add(user)
        
        return Response({"success": "Вы успешно зарегистрировались на хакатон"}, status=status.HTTP_200_OK)

class UnregisterFromHackathonView(APIView):
    """
    API для отмены регистрации на хакатон.
    """
    def post(self, request, hackathon_id):
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        user = request.user
        
        # Проверяем, открыта ли регистрация
        now = timezone.now().date()
        if now < hackathon.start_registation or now > hackathon.end_registration:
            return Response({"error": "Регистрация на этот хакатон закрыта"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, зарегистрирован ли пользователь
        if not hackathon.solo_participants.filter(id=user.id).exists():
            return Response({"error": "Вы не зарегистрированы на этот хакатон"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Отменяем регистрацию пользователя
        hackathon.solo_participants.remove(user)
        
        return Response({"success": "Вы успешно отменили регистрацию на хакатон"}, status=status.HTTP_200_OK)

class JoinTeamView(APIView):
    """
    API для присоединения к команде.
    """
    def post(self, request, join_code):
        team = get_object_or_404(Team, join_code=join_code)
        user = request.user
        
        # Проверяем, открыта ли команда
        if team.status == 'closed':
            return Response({"error": "Эта команда закрыта для новых участников"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, не заполнена ли команда
        if team.is_full:
            return Response({"error": "Команда уже заполнена"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, не состоит ли уже пользователь в этой команде
        if user in team.members.all():
            return Response({"error": "Вы уже состоите в этой команде"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, не состоит ли пользователь в другой команде этого хакатона
        if Team.objects.filter(hackathon=team.hackathon, members=user).exists():
            return Response({"error": "Вы уже состоите в другой команде этого хакатона"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Добавляем пользователя в команду
        team.members.add(user)
        
        return Response({"success": "Вы успешно присоединились к команде"}, status=status.HTTP_200_OK)

class LeaveTeamView(APIView):
    """
    API для выхода из команды.
    """
    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        user = request.user
        
        # Проверяем, состоит ли пользователь в этой команде
        if user not in team.members.all():
            return Response({"error": "Вы не состоите в этой команде"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, не является ли пользователь лидером команды
        if user == team.leader:
            return Response({"error": "Лидер не может покинуть команду. Передайте лидерство другому участнику или удалите команду"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Удаляем пользователя из команды
        team.members.remove(user)
        
        return Response({"success": "Вы успешно покинули команду"}, status=status.HTTP_200_OK)

class SubmitSolutionView(APIView):
    """
    API для отправки решения.
    """
    def post(self, request, solution_id):
        solution = get_object_or_404(Solution, id=solution_id)
        user = request.user
        
        # Проверяем, принадлежит ли решение пользователю или его команде
        if solution.user != user and (solution.team and user not in solution.team.members.all()):
            return Response({"error": "У вас нет прав на отправку этого решения"}, status=status.HTTP_403_FORBIDDEN)
        
        # Проверяем, не истек ли срок сдачи
        if solution.hackathon.submission_deadline and timezone.now() > solution.hackathon.submission_deadline:
            return Response({"error": "Срок сдачи решений истек"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Отправляем решение
        solution.status = 'submitted'
        solution.submitted_at = timezone.now()
        solution.save()
        
        return Response({"success": "Решение успешно отправлено"}, status=status.HTTP_200_OK)

class MySolutionsView(generics.ListAPIView):
    """
    API для просмотра своих решений.
    """
    serializer_class = SolutionSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Solution.objects.filter(user=user) | Solution.objects.filter(team__members=user)

class MyTeamsView(generics.ListAPIView):
    """
    API для просмотра своих команд.
    """
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(members=user)

class MyHackathonsView(generics.ListAPIView):
    """
    API для просмотра своих хакатонов.
    """
    serializer_class = HackathonSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Hackathon.objects.filter(solo_participants=user) | Hackathon.objects.filter(teams__members=user)