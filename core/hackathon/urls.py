from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'hackathon'

router = DefaultRouter()
router.register(r'hackathons', views.HackathonViewSet, basename='hackathon')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'prize-places', views.PrizePlacesViewSet, basename='prize-place')
router.register(r'tracks', views.TrackViewSet, basename='track')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'solutions', views.SolutionViewSet, basename='solution')
router.register(r'reviews', views.SolutionReviewViewSet, basename='review')
router.register(r'faqs', views.FAQViewSet, basename='faq')
router.register(r'live-streams', views.LiveStreamViewSet, basename='live-stream')

urlpatterns = [
    path('hackathons/register/<int:hackathon_id>/', views.RegisterForHackathonView.as_view(), name='register-for-hackathon'),
    path('hackathons/unregister/<int:hackathon_id>/', views.UnregisterFromHackathonView.as_view(), name='unregister-from-hackathon'),
    path('teams/join/<str:join_code>/', views.JoinTeamView.as_view(), name='join-team'),
    path('teams/leave/<int:team_id>/', views.LeaveTeamView.as_view(), name='leave-team'),
    path('solutions/submit/<int:solution_id>/', views.SubmitSolutionView.as_view(), name='submit-solution'),
    path('solutions/my/', views.MySolutionsView.as_view(), name='my-solutions'),
    path('teams/my/', views.MyTeamsView.as_view(), name='my-teams'),
    path('hackathons/my/', views.MyHackathonsView.as_view(), name='my-hackathons'),
]

urlpatterns += router.urls