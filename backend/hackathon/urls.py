from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HackathonViewSet, NewsViewSet,
    WebinarViewSet, CaseCupViewSet
)

router = DefaultRouter()
router.register(r'hackathons', HackathonViewSet, basename='hackathon')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'webinars', WebinarViewSet, basename='webinar')
router.register(r'case-cups', CaseCupViewSet, basename='casecup')

urlpatterns = [
    path('', include(router.urls)),
] 