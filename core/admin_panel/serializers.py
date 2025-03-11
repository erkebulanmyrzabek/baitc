from rest_framework import serializers
from .models import AdminRole, HackathonRequest, UserBlock, AdminLog, Analytics, OrganizerDashboard
from user.serializers import UserSerializer
from hackathon.serializers import HackathonSerializer

class AdminRoleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    
    class Meta:
        model = AdminRole
        fields = ['id', 'user', 'role', 'assigned_by', 'assigned_at']

class AdminRoleCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AdminRole
        fields = ['user_id', 'role']
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        assigned_by = self.context['request'].user
        admin_role = AdminRole.objects.create(user_id=user_id, assigned_by=assigned_by, **validated_data)
        return admin_role

class HackathonRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = HackathonRequest
        fields = [
            'id', 'user', 'title', 'description', 'expected_start_date',
            'expected_end_date', 'expected_participants', 'prize_pool',
            'status', 'reviewed_by', 'reviewed_at', 'created_at', 'comment'
        ]

class HackathonRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonRequest
        fields = [
            'title', 'description', 'expected_start_date', 'expected_end_date',
            'expected_participants', 'prize_pool'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        hackathon_request = HackathonRequest.objects.create(user=user, **validated_data)
        return hackathon_request

class UserBlockSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    blocked_by = UserSerializer(read_only=True)
    
    class Meta:
        model = UserBlock
        fields = ['id', 'user', 'reason', 'blocked_by', 'blocked_at', 'unblocked_at', 'is_active']

class UserBlockCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserBlock
        fields = ['user_id', 'reason']
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        blocked_by = self.context['request'].user
        user_block = UserBlock.objects.create(user_id=user_id, blocked_by=blocked_by, **validated_data)
        return user_block

class AdminLogSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    
    class Meta:
        model = AdminLog
        fields = ['id', 'admin', 'action', 'details', 'created_at']

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = [
            'id', 'date', 'active_users', 'new_users', 'hackathons_count',
            'teams_count', 'solutions_count', 'transactions_count',
            'total_revenue', 'premium_users_count'
        ]

class OrganizerDashboardSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    hackathons = HackathonSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrganizerDashboard
        fields = [
            'id', 'organizer', 'hackathons', 'total_participants',
            'total_teams', 'total_solutions', 'average_rating'
        ] 