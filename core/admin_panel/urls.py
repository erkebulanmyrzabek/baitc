from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'admin_panel'

router = DefaultRouter()
router.register(r'admin-roles', views.AdminRoleViewSet, basename='admin-role')
router.register(r'hackathon-requests', views.HackathonRequestViewSet, basename='hackathon-request')
router.register(r'user-blocks', views.UserBlockViewSet, basename='user-block')
router.register(r'admin-logs', views.AdminLogViewSet, basename='admin-log')
router.register(r'analytics', views.AnalyticsViewSet, basename='analytics')
router.register(r'organizer-dashboard', views.OrganizerDashboardViewSet, basename='organizer-dashboard')

urlpatterns = [
    path('hackathon-requests/approve/<int:request_id>/', views.ApproveHackathonRequestView.as_view(), name='approve-hackathon-request'),
    path('hackathon-requests/reject/<int:request_id>/', views.RejectHackathonRequestView.as_view(), name='reject-hackathon-request'),
    path('user-blocks/block/<int:user_id>/', views.BlockUserView.as_view(), name='block-user'),
    path('user-blocks/unblock/<int:user_id>/', views.UnblockUserView.as_view(), name='unblock-user'),
    path('admin-roles/assign/', views.AssignAdminRoleView.as_view(), name='assign-admin-role'),
    path('admin-roles/revoke/<int:role_id>/', views.RevokeAdminRoleView.as_view(), name='revoke-admin-role'),
    path('analytics/users/', views.UserAnalyticsView.as_view(), name='user-analytics'),
    path('analytics/hackathons/', views.HackathonAnalyticsView.as_view(), name='hackathon-analytics'),
    path('analytics/shop/', views.ShopAnalyticsView.as_view(), name='shop-analytics'),
]

urlpatterns += router.urls
