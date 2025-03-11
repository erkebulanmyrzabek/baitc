from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'community'

router = DefaultRouter()
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'friendships', views.FriendshipViewSet, basename='friendship')
router.register(r'leaderboards', views.LeaderboardViewSet, basename='leaderboard')
router.register(r'events', views.CommunityEventViewSet, basename='event')

urlpatterns = [
    path('teams/join/<str:team_id>/', views.JoinTeamView.as_view(), name='join-team'),
    path('teams/leave/<str:team_id>/', views.LeaveTeamView.as_view(), name='leave-team'),
    path('teams/my/', views.MyTeamsView.as_view(), name='my-teams'),
    path('friendships/pending/', views.PendingFriendshipsView.as_view(), name='pending-friendships'),
    path('friendships/accept/<int:friendship_id>/', views.AcceptFriendshipView.as_view(), name='accept-friendship'),
    path('friendships/reject/<int:friendship_id>/', views.RejectFriendshipView.as_view(), name='reject-friendship'),
    path('events/register/<int:event_id>/', views.RegisterForEventView.as_view(), name='register-for-event'),
    path('events/unregister/<int:event_id>/', views.UnregisterFromEventView.as_view(), name='unregister-from-event'),
    path('search/users/', views.UserSearchView.as_view(), name='search-users'),
]

urlpatterns += router.urls 