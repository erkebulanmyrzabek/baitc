from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

user_img_url = FileSystemStorage(
    location=os.path.join(settings.BASE_DIR, 'static', 'img', 'user_img'),  
    base_url='/static/img/user_img'
)

class User(models.Model):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Темная')
    ]
    
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'Английский')
    ]
    
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    coin = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    is_premium = models.BooleanField(default=False)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru')
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    def add_xp(self, amount):
        """Добавляет опыт пользователю и обновляет уровень"""
        self.xp += amount
        self.save()
    
    def xp_to_next_level(self):
        """Возвращает количество XP, необходимое для достижения следующего уровня"""
        return (self.level + 1) * 100 - self.xp
    
    def participation_count(self):
        """Возвращает количество хакатонов, в которых участвовал пользователь"""
        return self.hackathons.count()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
