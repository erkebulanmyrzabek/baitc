from rest_framework import serializers
from .models import UserProfile, TechStack, Achievement

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['id', 'name']

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'title', 'description', 'icon_url', 'date_earned']

class UserProfileSerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    friends_count = serializers.SerializerMethodField()
    hackathons_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'telegram_id', 'username', 'first_name', 'last_name',
            'photo_url', 'phone', 'city', 'age', 'gender',
            'tech_stack', 'language', 'theme', 'xp', 'level',
            'crystals', 'achievements', 'friends_count',
            'hackathons_count'
        ]
        read_only_fields = [
            'telegram_id', 'xp', 'level', 'crystals',
            'achievements', 'friends_count', 'hackathons_count'
        ]

    def get_friends_count(self, obj):
        return obj.friends.count()

    def get_hackathons_count(self, obj):
        return obj.hackathons.count()

    def validate_age(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Возраст не может быть отрицательным")
        return value

    def validate_phone(self, value):
        if value and not value.startswith('+'):
            raise serializers.ValidationError("Номер телефона должен начинаться с '+'")
        return value

class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_null=True)
    photo_url = serializers.URLField(required=False, allow_null=True)

    def create(self, validated_data):
        user, created = UserProfile.objects.get_or_create(
            telegram_id=validated_data['telegram_id'],
            defaults={
                'first_name': validated_data.get('first_name', ''),
                'last_name': validated_data.get('last_name', ''),
                'username': validated_data.get('username'),
                'photo_url': validated_data.get('photo_url')
            }
        )
        if not created:
            # Обновляем существующего пользователя
            for field in ['first_name', 'last_name', 'username', 'photo_url']:
                if field in validated_data:
                    setattr(user, field, validated_data[field])
            user.save()
        return user
