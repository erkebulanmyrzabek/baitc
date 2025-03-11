from rest_framework import serializers
from .models import Hackathon

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