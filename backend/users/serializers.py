from rest_framework import serializers
from .models import UserProfile, Achievement, TechStack, UserAchievement, UserTechStack

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon']

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()
    
    class Meta:
        model = UserAchievement
        fields = ['achievement', 'unlocked', 'unlocked_date']

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['id', 'name', 'icon']

class UserTechStackSerializer(serializers.ModelSerializer):
    tech = TechStackSerializer()
    
    class Meta:
        model = UserTechStack
        fields = ['tech', 'level']

class UserProfileSerializer(serializers.ModelSerializer):
    achievements = UserAchievementSerializer(source='userachievement_set', many=True, read_only=True)
    tech_stack = UserTechStackSerializer(source='usertechstack_set', many=True, read_only=True)
    hackathons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'photo', 'telegram_id', 'achievements', 'tech_stack', 'hackathons_count']
    
    def get_hackathons_count(self, obj):
        # Здесь нужно добавить логику подсчета хакатонов
        return 0  # Временное значение 