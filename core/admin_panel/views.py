from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AdminRole, HackathonRequest, UserBlock, AdminLog, Analytics, OrganizerDashboard
from .serializers import (
    AdminRoleSerializer, AdminRoleCreateSerializer, HackathonRequestSerializer,
    HackathonRequestCreateSerializer, UserBlockSerializer, UserBlockCreateSerializer,
    AdminLogSerializer, AnalyticsSerializer, OrganizerDashboardSerializer
)
from user.models import User
from hackathon.models import Hackathon
from django.db import models

class IsAdmin(permissions.BasePermission):
    """
    Проверка, является ли пользователь администратором.
    """
    def has_permission(self, request, view):
        return AdminRole.objects.filter(user=request.user).exists()

class HasAdminRole(permissions.BasePermission):
    """
    Проверка, имеет ли пользователь определенную роль администратора.
    """
    def __init__(self, required_roles):
        self.required_roles = required_roles
    
    def has_permission(self, request, view):
        return AdminRole.objects.filter(user=request.user, role__in=self.required_roles).exists()

class AdminRoleViewSet(viewsets.ModelViewSet):
    """
    API для работы с ролями администраторов.
    """
    serializer_class = AdminRoleSerializer
    permission_classes = [HasAdminRole(['admin'])]
    
    def get_queryset(self):
        return AdminRole.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AdminRoleCreateSerializer
        return AdminRoleSerializer
    
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class AssignAdminRoleView(APIView):
    """
    API для назначения роли администратора.
    """
    permission_classes = [HasAdminRole(['admin'])]
    
    def post(self, request):
        serializer = AdminRoleCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        admin_role = serializer.save()
        
        # Логируем действие
        AdminLog.objects.create(
            admin=request.user,
            action='assign_admin_role',
            details=f"Назначена роль {admin_role.get_role_display()} пользователю {admin_role.user.name}"
        )
        
        return Response(AdminRoleSerializer(admin_role).data, status=status.HTTP_201_CREATED)

class RevokeAdminRoleView(APIView):
    """
    API для отзыва роли администратора.
    """
    permission_classes = [HasAdminRole(['admin'])]
    
    def post(self, request, role_id):
        admin_role = get_object_or_404(AdminRole, id=role_id)
        
        # Логируем действие
        AdminLog.objects.create(
            admin=request.user,
            action='revoke_admin_role',
            details=f"Отозвана роль {admin_role.get_role_display()} у пользователя {admin_role.user.name}"
        )
        
        admin_role.delete()
        
        return Response({"success": "Роль администратора отозвана"}, status=status.HTTP_200_OK)

class HackathonRequestViewSet(viewsets.ModelViewSet):
    """
    API для работы с запросами на проведение хакатонов.
    """
    serializer_class = HackathonRequestSerializer
    
    def get_queryset(self):
        if AdminRole.objects.filter(user=self.request.user).exists():
            return HackathonRequest.objects.all()
        return HackathonRequest.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return HackathonRequestCreateSerializer
        return HackathonRequestSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ApproveHackathonRequestView(APIView):
    """
    API для одобрения запроса на проведение хакатона.
    """
    permission_classes = [HasAdminRole(['admin', 'moderator'])]
    
    def post(self, request, request_id):
        hackathon_request = get_object_or_404(HackathonRequest, id=request_id)
        
        if hackathon_request.status != 'pending':
            return Response({"error": "Этот запрос уже обработан"}, status=status.HTTP_400_BAD_REQUEST)
        
        hackathon_request.status = 'approved'
        hackathon_request.reviewed_by = request.user
        hackathon_request.reviewed_at = timezone.now()
        hackathon_request.save()
        
        # Логируем действие
        AdminLog.objects.create(
            admin=request.user,
            action='approve_hackathon_request',
            details=f"Одобрен запрос на проведение хакатона '{hackathon_request.title}'"
        )
        
        return Response(HackathonRequestSerializer(hackathon_request).data, status=status.HTTP_200_OK)

class RejectHackathonRequestView(APIView):
    """
    API для отклонения запроса на проведение хакатона.
    """
    permission_classes = [HasAdminRole(['admin', 'moderator'])]
    
    def post(self, request, request_id):
        hackathon_request = get_object_or_404(HackathonRequest, id=request_id)
        
        if hackathon_request.status != 'pending':
            return Response({"error": "Этот запрос уже обработан"}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = request.data.get('comment', '')
        
        hackathon_request.status = 'rejected'
        hackathon_request.reviewed_by = request.user
        hackathon_request.reviewed_at = timezone.now()
        hackathon_request.comment = comment
        hackathon_request.save()
        
        # Логируем действие
        AdminLog.objects.create(
            admin=request.user,
            action='reject_hackathon_request',
            details=f"Отклонен запрос на проведение хакатона '{hackathon_request.title}'"
        )
        
        return Response(HackathonRequestSerializer(hackathon_request).data, status=status.HTTP_200_OK)

class UserBlockViewSet(viewsets.ModelViewSet):
    """
    API для работы с блокировками пользователей.
    """
    serializer_class = UserBlockSerializer
    permission_classes = [HasAdminRole(['admin', 'moderator'])]
    
    def get_queryset(self):
        return UserBlock.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserBlockCreateSerializer
        return UserBlockSerializer
    
    def perform_create(self, serializer):
        serializer.save(blocked_by=self.request.user)

class BlockUserView(APIView):
    """
    API для блокировки пользователя.
    """
    permission_classes = [HasAdminRole(['admin', 'moderator'])]
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        reason = request.data.get('reason', '')
        
        # Проверяем, не заблокирован ли уже пользователь
        if UserBlock.objects.filter(user=user, is_active=True).exists():
            return Response({"error": "Этот пользователь уже заблокирован"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_block = UserBlock.objects.create(
            user=user,
            reason=reason,
            blocked_by=request.user
        )
        
        # Логируем действие
        AdminLog.objects.create(
            admin=request.user,
            action='block_user',
            details=f"Заблокирован пользователь {user.name}"
        )
        
        return Response(UserBlockSerializer(user_block).data, status=status.HTTP_201_CREATED)

class UnblockUserView(APIView):
    """
    API для разблокировки пользователя.
    """
    permission_classes = [HasAdminRole(['admin', 'moderator'])]
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Находим активную блокировку
        try:
            user_block = UserBlock.objects.get(user=user, is_active=True)
        except UserBlock.DoesNotExist:
            return Response({"error": "Этот пользователь не заблокирован"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_block.is_active = False
        user_block.unblocked_at = timezone.now()
        user_block.save()
        
        # Логируем действие
        AdminLog.objects.create(
            admin=request.user,
            action='unblock_user',
            details=f"Разблокирован пользователь {user.name}"
        )
        
        return Response(UserBlockSerializer(user_block).data, status=status.HTTP_200_OK)

class AdminLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра логов администраторов.
    """
    serializer_class = AdminLogSerializer
    permission_classes = [HasAdminRole(['admin'])]
    
    def get_queryset(self):
        return AdminLog.objects.all().order_by('-created_at')

class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра аналитики.
    """
    serializer_class = AnalyticsSerializer
    permission_classes = [HasAdminRole(['admin', 'analyst'])]
    
    def get_queryset(self):
        return Analytics.objects.all().order_by('-date')

class OrganizerDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра дашборда организатора.
    """
    serializer_class = OrganizerDashboardSerializer
    permission_classes = [HasAdminRole(['admin', 'organizer'])]
    
    def get_queryset(self):
        if AdminRole.objects.filter(user=self.request.user, role='admin').exists():
            return OrganizerDashboard.objects.all()
        return OrganizerDashboard.objects.filter(organizer=self.request.user)

class UserAnalyticsView(APIView):
    """
    API для просмотра аналитики по пользователям.
    """
    permission_classes = [HasAdminRole(['admin', 'analyst'])]
    
    def get(self, request):
        total_users = User.objects.count()
        premium_users = User.objects.filter(is_premium=True).count()
        new_users_today = User.objects.filter(created_at__date=timezone.now().date()).count()
        
        return Response({
            "total_users": total_users,
            "premium_users": premium_users,
            "premium_percentage": round(premium_users / total_users * 100, 2) if total_users > 0 else 0,
            "new_users_today": new_users_today
        })

class HackathonAnalyticsView(APIView):
    """
    API для просмотра аналитики по хакатонам.
    """
    permission_classes = [HasAdminRole(['admin', 'analyst', 'organizer'])]
    
    def get(self, request):
        total_hackathons = Hackathon.objects.count()
        active_hackathons = Hackathon.objects.filter(status='active').count()
        upcoming_hackathons = Hackathon.objects.filter(status='upcoming').count()
        finished_hackathons = Hackathon.objects.filter(status='finished').count()
        
        return Response({
            "total_hackathons": total_hackathons,
            "active_hackathons": active_hackathons,
            "upcoming_hackathons": upcoming_hackathons,
            "finished_hackathons": finished_hackathons
        })

class ShopAnalyticsView(APIView):
    """
    API для просмотра аналитики по магазину.
    """
    permission_classes = [HasAdminRole(['admin', 'analyst'])]
    
    def get(self, request):
        from shop.models import Transaction
        
        total_transactions = Transaction.objects.count()
        total_revenue = Transaction.objects.filter(status='completed').aggregate(total=models.Sum('total_price'))['total'] or 0
        
        return Response({
            "total_transactions": total_transactions,
            "total_revenue": total_revenue
        })
