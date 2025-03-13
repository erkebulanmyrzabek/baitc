from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from django.utils import timezone
from .serializers import HackathonSerializer
from .models import Hackathon
import logging
from django.conf import settings
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated, AllowAny

logger = logging.getLogger(__name__)



class HackathonViewSet(viewsets.ModelViewSet):
    serializer_class = HackathonSerializer
    search_fields = ['name', 'short_description', 'full_description', 'requirements', 'location']
    ordering_fields = ['start_date', 'created_at', 'name']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'register', 'unregister']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        try:
            cache_key = 'hackathon_queryset'
            queryset = cache.get(cache_key)
            
            if queryset is None:
                logger.info("Cache miss for hackathon queryset")
                queryset = Hackathon.objects.prefetch_related('participants', 'tags').all()
                cache.set(cache_key, queryset, timeout=300)  # кэшируем на 5 минут
            
            return queryset
        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}")
            return Hackathon.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            logger.info("Attempting to fetch hackathons list")
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info(f"Successfully retrieved {len(page)} hackathons")
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            logger.info(f"Successfully retrieved {len(queryset)} hackathons")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching hackathons list: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при получении списка хакатонов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def active(self, request):
        try:
            cache_key = 'active_hackathons'
            queryset = cache.get(cache_key)
            
            if queryset is None:
                logger.info("Cache miss for active hackathons")
                now = timezone.now()
                queryset = self.get_queryset().filter(
                    end_date__gte=now
                ).order_by('start_date')
                cache.set(cache_key, queryset, timeout=300)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching active hackathons: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при получении списка активных хакатонов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        try:
            hackathon = self.get_object()
            user = request.user

            if hackathon.participants.filter(id=user.id).exists():
                return Response(
                    {"error": "Вы уже зарегистрированы на этот хакатон"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if hackathon.registration_deadline < timezone.now():
                return Response(
                    {"error": "Регистрация на этот хакатон уже закрыта"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if hackathon.participants.count() >= hackathon.max_participants:
                return Response(
                    {"error": "Достигнуто максимальное количество участников"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            hackathon.participants.add(user)
            logger.info(f"User {user.id} successfully registered for hackathon {hackathon.id}")
            return Response({"message": "Вы успешно зарегистрировались на хакатон"})
        except Exception as e:
            logger.error(f"Error during hackathon registration: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при регистрации на хакатон"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        try:
            hackathon = self.get_object()
            user = request.user

            if not hackathon.participants.filter(id=user.id).exists():
                return Response(
                    {"error": "Вы не зарегистрированы на этот хакатон"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if hackathon.start_date < timezone.now():
                return Response(
                    {"error": "Нельзя отменить регистрацию после начала хакатона"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            hackathon.participants.remove(user)
            logger.info(f"User {user.id} successfully unregistered from hackathon {hackathon.id}")
            return Response({"message": "Регистрация успешно отменена"})
        except Exception as e:
            logger.error(f"Error during hackathon unregistration: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при отмене регистрации"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
