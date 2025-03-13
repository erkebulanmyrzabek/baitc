from rest_framework import serializers
from django.utils import timezone
from .models import Hackathon, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class HackathonSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    participants_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    can_register = serializers.SerializerMethodField()
    image = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = Hackathon
        fields = [
            'id', 'name', 'full_description', 'short_description', 'image',
            'start_date', 'end_date', 'registration_deadline', 'max_participants',
            'prize_pool', 'location', 'is_online', 'tags', 'requirements',
            'participants_count', 'is_registered', 'can_register',
            'created_at', 'updated_at'
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
            if obj.registration_deadline < now:
                return False
            if obj.participants.count() >= obj.max_participants:
                return False
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                return not obj.participants.filter(id=request.user.id).exists()
            return True
        except Exception as e:
            return False

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError({
                    "end_date": "Дата окончания должна быть позже даты начала"
                })

        if 'registration_deadline' in data and 'start_date' in data:
            if data['registration_deadline'] >= data['start_date']:
                raise serializers.ValidationError({
                    "registration_deadline": "Дедлайн регистрации должен быть раньше даты начала"
                })

        if 'max_participants' in data and data['max_participants'] < 1:
            raise serializers.ValidationError({
                "max_participants": "Максимальное количество участников должно быть больше 0"
            })


        return data