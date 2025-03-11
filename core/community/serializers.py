from rest_framework import serializers
from .models import Team, Friendship, Leaderboard, CommunityEvent, UserSearch
from user.serializers import UserSerializer

class TeamSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    members_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'leader', 'members', 'max_members',
            'status', 'created_at', 'members_count', 'is_full'
        ]

class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description', 'max_members', 'status']
    
    def create(self, validated_data):
        user = self.context['request'].user
        team = Team.objects.create(leader=user, **validated_data)
        team.members.add(user)
        return team

class FriendshipSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']

class FriendshipCreateSerializer(serializers.ModelSerializer):
    receiver_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Friendship
        fields = ['receiver_id']
    
    def validate(self, data):
        sender = self.context['request'].user
        receiver_id = data.get('receiver_id')
        
        if sender.id == receiver_id:
            raise serializers.ValidationError("Вы не можете отправить запрос на дружбу самому себе.")
        
        if Friendship.objects.filter(sender=sender, receiver_id=receiver_id).exists():
            raise serializers.ValidationError("Вы уже отправили запрос на дружбу этому пользователю.")
        
        if Friendship.objects.filter(sender_id=receiver_id, receiver=sender).exists():
            raise serializers.ValidationError("Этот пользователь уже отправил вам запрос на дружбу.")
        
        return data
    
    def create(self, validated_data):
        sender = self.context['request'].user
        receiver_id = validated_data.pop('receiver_id')
        friendship = Friendship.objects.create(sender=sender, receiver_id=receiver_id, **validated_data)
        return friendship

class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'user', 'period', 'score', 'rank', 'hackathons_won',
            'hackathons_participated', 'created_at'
        ]

class CommunityEventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    participants_count = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CommunityEvent
        fields = [
            'id', 'title', 'description', 'event_type', 'start_date', 'end_date',
            'location', 'is_online', 'online_url', 'organizer', 'participants',
            'max_participants', 'created_at', 'participants_count', 'is_full',
            'is_past', 'is_ongoing'
        ]

class CommunityEventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEvent
        fields = [
            'title', 'description', 'event_type', 'start_date', 'end_date',
            'location', 'is_online', 'online_url', 'max_participants'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        event = CommunityEvent.objects.create(organizer=user, **validated_data)
        return event

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearch
        fields = ['id', 'user', 'query', 'created_at'] 