from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import telegram_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hackathon.urls')),
    path('api/users/', include('users.urls')),
    path('api/auth/telegram/', telegram_auth, name='telegram-auth-alt'),  # Альтернативный путь
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
