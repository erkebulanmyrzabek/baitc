from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from .models import Hackathon
from .serializers import HackathonSerializer

# Create your views here.

class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'name']
    ordering = ['-start_date']  
    
    def get_queryset(self):
        """
        Получаем хакатоны с учетом кэширования
        """
        cache_key = 'hackathons_list'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            queryset = Hackathon.objects.all()
            # Кэшируем на 15 минут
            cache.set(cache_key, queryset, timeout=900)
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Получение списка хакатонов с обработкой ошибок
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Произошла ошибка при получении списка хакатонов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Получение только активных хакатонов
        """
        try:
            today = timezone.now().date()
            
            cache_key = 'active_hackathons'
            queryset = cache.get(cache_key)
            
            if queryset is None:
                queryset = self.get_queryset().filter(
                    end_date__gte=today
                ).order_by('start_date')
                cache.set(cache_key, queryset, timeout=900)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Произошла ошибка при получении активных хакатонов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
