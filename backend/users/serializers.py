from rest_framework import serializers
from .models import UserProfile

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['telegram_id', 'username', 'first_name', 'last_name', 
                 'photo_url', 'phone', 'city', 'age', 'gender', 
                 'tech_stack', 'language', 'theme', 'xp', 'level']
        read_only_fields = ['telegram_id', 'xp', 'level']
