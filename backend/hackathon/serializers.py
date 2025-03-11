from rest_framework import serializers
from .models import Hackathon, News, Webinar, CaseCup

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ['id', 'name', 'description', 'start_date', 'end_date']
        
    def validate(self, data):
        """
        Проверяем, что дата начала раньше даты окончания
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                "end_date": "Дата окончания должна быть позже даты начала"
            })
        return data

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image_url', 'created_at', 'updated_at']

class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = ['id', 'title', 'description', 'speaker', 'date', 'duration', 'link', 'image_url']

    def validate_date(self, value):
        """
        Проверяем, что дата вебинара не в прошлом
        """
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Дата вебинара не может быть в прошлом")
        return value

class CaseCupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseCup
        fields = ['id', 'name', 'description', 'company', 'prize_fund', 
                 'start_date', 'end_date', 'registration_deadline', 'image_url']

    def validate(self, data):
        """
        Проверяем корректность дат
        """
        if data['registration_deadline'] > data['start_date']:
            raise serializers.ValidationError({
                "registration_deadline": "Дедлайн регистрации должен быть до начала кейс-чемпионата"
            })
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                "end_date": "Дата окончания должна быть позже даты начала"
            })
        return data