from rest_framework import serializers
from .models import User, Skill, Achievement, Certificate, UserNotification

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon', 'xp_reward', 'crystal_reward']

class CertificateSerializer(serializers.ModelSerializer):
    event_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Certificate
        fields = ['id', 'user', 'hackathon', 'webinar', 'casecup', 'issue_date', 'certificate_file', 'event_name']
    
    def get_event_name(self, obj):
        if obj.hackathon:
            return obj.hackathon.name
        elif obj.webinar:
            return obj.webinar.name
        elif obj.casecup:
            return obj.casecup.name
        return "Неизвестное событие"

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['id', 'user', 'type', 'title', 'message', 'is_read', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    notifications = UserNotificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'telegram_id', 'name', 'coin', 'hash_code', 'xp', 'level',
            'avatar', 'skills', 'achievements', 'friends', 'is_premium',
            'theme', 'language', 'bio', 'email', 'certificates', 'notifications'
        ]
        read_only_fields = ['coin', 'hash_code', 'xp', 'level', 'is_premium']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_id', 'name', 'email', 'bio', 'theme', 'language']
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    xp_to_next_level = serializers.SerializerMethodField()
    participation_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'name', 'coin', 'hash_code', 'xp', 'level', 'avatar',
            'skills', 'achievements', 'is_premium', 'theme', 'language',
            'bio', 'email', 'xp_to_next_level', 'participation_count'
        ]
    
    def get_xp_to_next_level(self, obj):
        return obj.xp_to_next_level()
    
    def get_participation_count(self, obj):
        return obj.participation_count()

class UserLoginSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    
    def validate(self, data):
        telegram_id = data.get('telegram_id')
        
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким Telegram ID не найден.")
        
        data['user'] = user
        return data 