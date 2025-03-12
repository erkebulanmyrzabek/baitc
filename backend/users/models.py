from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class User(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Мужской'),
            ('female', 'Женский'),
            ('other', 'Другой')
        ],
        blank=True,
        null=True
    )
    tech_stack = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        default=list
    )
    language = models.CharField(
        max_length=5,
        choices=[
            ('ru', 'Русский'),
            ('en', 'English'),
            ('kk', 'Қазақша')
        ],
        default='ru'
    )
    theme = models.CharField(
        max_length=10,
        choices=[
            ('system', 'Системная'),
            ('light', 'Светлая'),
            ('dark', 'Темная')
        ],
        default='system'
    )
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.username} ({self.telegram_id})"
    
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
    
    def level_up(self):
        """Повышает уровень пользователя"""
        self.level += 1
        self.save()
