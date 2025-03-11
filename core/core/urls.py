from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Hackathon Platform API",
        default_version='v1',
        description="API для платформы хакатонов и Telegram Mini App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@hackathonplatform.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/', include('feed.urls')),
    path('hackathon/', include('hackathon.urls')),
    path('rating/', include('rating.urls')),
    
    # API маршруты
    path('api/user/', include('user.urls')),
    path('api/feed/', include('feed.urls', namespace='feed_api')),
    path('api/hackathon/', include('hackathon.urls', namespace='hackathon_api')),
    path('api/shop/', include('shop.urls')),
    path('api/community/', include('community.urls')),
    path('api/rating/', include('rating.urls', namespace='rating_api')),
    path('api/admin_panel/', include('admin_panel.urls')),
    
    # Документация API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Добавляем маршруты для медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
