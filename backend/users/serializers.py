from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    photo_url = serializers.URLField(required=False, allow_null=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'telegram_id', 'photo_url', 'phone', 'city', 'age',
            'gender', 'tech_stack', 'language', 'theme'
        ]
        read_only_fields = ['id', 'telegram_id']

    def validate_age(self, value):
        if value and (value < 0 or value > 120):
            raise serializers.ValidationError("Возраст должен быть между 0 и 120")
        return value

    def validate_phone(self, value):
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Неверный формат номера телефона")
        return value
