from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from . import telegram_api

app_name = 'user'

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'skills', views.SkillViewSet, basename='skill')
router.register(r'achievements', views.AchievementViewSet, basename='achievement')
router.register(r'certificates', views.CertificateViewSet, basename='certificate')
router.register(r'notifications', views.UserNotificationViewSet, basename='notification')

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('friends/', views.FriendsListView.as_view(), name='friends-list'),
    path('friends/add/<str:hash_code>/', views.AddFriendView.as_view(), name='add-friend'),
    path('friends/remove/<str:hash_code>/', views.RemoveFriendView.as_view(), name='remove-friend'),
    path('achievements/unlock/<int:achievement_id>/', views.UnlockAchievementView.as_view(), name='unlock-achievement'),
    path('telegram/login/', telegram_api.TelegramLoginView.as_view(), name='telegram-login'),
    path('telegram/profile/', telegram_api.TelegramUserProfileView.as_view(), name='telegram-profile'),
    path('telegram/init-data/', telegram_api.TelegramInitDataView.as_view(), name='telegram-init-data'),
    path('telegram/webapp-data/', telegram_api.TelegramWebAppDataView.as_view(), name='telegram-webapp-data'),
]

urlpatterns += router.urls 