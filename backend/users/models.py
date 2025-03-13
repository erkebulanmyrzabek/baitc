from django.db import models
import json
from django.conf import settings

class UserProfile(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
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
    tech_stack = models.TextField(blank=True, default='[]')  # Будет хранить JSON
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
    
    def get_tech_stack(self):
        """Получить список технологий"""
        try:
            return json.loads(self.tech_stack)
        except:
            return []
    
    def set_tech_stack(self, tech_list):
        """Установить список технологий"""
        self.tech_stack = json.dumps(tech_list)
    
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

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
