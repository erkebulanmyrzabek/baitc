from django.db import models
import json

class TechStack(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    date_earned = models.DateField(auto_now_add=True)

class UserProfile(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    tech_stack = models.ManyToManyField(TechStack, related_name='users', blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Мужской'),
            ('female', 'Женский'),
        ],
        blank=True,
        null=True
    )
    language = models.CharField(
        max_length=5,
        choices=[
            ('ru', 'Русский'),
            ('en', 'English'),
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
        default='light'
    )
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    crystals = models.PositiveIntegerField(default=0)
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friend_of', blank=True)

    def __str__(self):
        return f"{self.username} ({self.telegram_id})"

    def add_xp(self, amount):
        """Добавляет опыт пользователю и обновляет уровень"""
        self.xp += amount
        if self.xp >= self.xp_to_next_level():
            self.level_up()
        self.save()

    def xp_to_next_level(self):
        """Возвращает количество XP, необходимое для достижения следующего уровня"""
        return (self.level + 1) * 100

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
