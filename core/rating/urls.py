from django.urls import path
from .views import rating_view

app_name = 'rating'

urlpatterns = [
    path('', rating_view, name='rating'),
] 