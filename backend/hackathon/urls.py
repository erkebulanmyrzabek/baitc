from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HackathonViewSet
)

router = DefaultRouter()
router.register(r'hackathons', HackathonViewSet, basename='hackathon')

urlpatterns = [
    path('', include(router.urls)),
] 