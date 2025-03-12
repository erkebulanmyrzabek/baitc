from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'avatar', 'email', 'coin', 'xp', 'level', 'theme', 'language']
        read_only_fields = ['coin', 'xp', 'level']
