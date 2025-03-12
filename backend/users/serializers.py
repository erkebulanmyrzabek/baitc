from rest_framework import serializers
from .models import UserProfile
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    photo_url = serializers.URLField(required=False, allow_null=True)

class UserProfileSerializer(serializers.ModelSerializer):
    tech_stack = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'telegram_id', 'username', 'first_name', 'last_name',
            'photo_url', 'phone', 'city', 'age', 'gender',
            'tech_stack', 'language', 'theme', 'xp', 'level'
        ]
        read_only_fields = ['id', 'telegram_id', 'xp', 'level']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['tech_stack'] = instance.get_tech_stack()
        return ret

    def to_internal_value(self, data):
        if 'tech_stack' in data:
            tech_stack = data.pop('tech_stack')
            internal_data = super().to_internal_value(data)
            internal_data['tech_stack'] = json.dumps(tech_stack)
            return internal_data
        return super().to_internal_value(data)

    def validate_age(self, value):
        if value and (value < 0 or value > 120):
            raise serializers.ValidationError("Возраст должен быть между 0 и 120")
        return value

    def validate_phone(self, value):
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Неверный формат номера телефона")
        return value
