from rest_framework import serializers
from django.utils import timezone
from .models import Hackathon, Tag, HackathonTime, HackathonImages

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class HackathonTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonTime
        fields = ['start_date', 'end_date', 'registration_deadline']

class HackathonImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonImages
        fields = ['preview_image', 'banner_image', 'cover_image', 'thumbnail_image']

class HackathonSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    time_info = HackathonTimeSerializer(read_only=True)
    images = HackathonImagesSerializer(read_only=True)
    participants_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    can_register = serializers.SerializerMethodField()
    
    class Meta:
        model = Hackathon
        fields = [
            'id', 'name', 'full_description', 'short_description',
            'type', 'status', 'registration_limit', 'prize_pool',
            'location', 'tags', 'participants_count', 'is_registered',
            'can_register', 'time_info', 'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['participants_count', 'is_registered', 'can_register', 'created_at', 'updated_at']

    def get_participants_count(self, obj):
        try:
            return obj.participants.count()
        except Exception as e:
            return 0

    def get_is_registered(self, obj):
        try:
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                return obj.participants.filter(id=request.user.id).exists()
            return False
        except Exception as e:
            return False

    def get_can_register(self, obj):
        try:
            now = timezone.now()
            if not hasattr(obj, 'time_info') or not obj.time_info:
                return False
            if obj.time_info.registration_deadline < now:
                return False
            if obj.registration_limit and obj.participants.count() >= obj.registration_limit:
                return False
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                return not obj.participants.filter(id=request.user.id).exists()
            return True
        except Exception as e:
            return False

    def validate(self, data):
        if 'time_info' in data:
            time_info = data['time_info']
            if time_info['start_date'] >= time_info['end_date']:
                raise serializers.ValidationError({
                    "time_info": {"end_date": "Дата окончания должна быть позже даты начала"}
                })

            if time_info['registration_deadline'] >= time_info['start_date']:
                raise serializers.ValidationError({
                    "time_info": {"registration_deadline": "Дедлайн регистрации должен быть раньше даты начала"}
                })

        if 'registration_limit' in data and data['registration_limit'] is not None and data['registration_limit'] < 1:
            raise serializers.ValidationError({
                "registration_limit": "Лимит участников должен быть больше 0"
            })

        return data