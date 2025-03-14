from django.db import models
from django.core.validators import MinValueValidator

from users.models import UserProfile

class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class HackathonTime(models.Model):
    hackathon = models.OneToOneField(
        'Hackathon',
        on_delete=models.CASCADE,
        related_name='time_info'
    )
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    registration_deadline = models.DateTimeField('Дедлайн регистрации')
    
    class Meta:
        verbose_name = 'Время проведения хакатона'
        verbose_name_plural = 'Время проведения хакатонов'

    def __str__(self):
        return f"Расписание для {self.hackathon.name}"

class HackathonImages(models.Model):
    hackathon = models.OneToOneField('Hackathon', on_delete=models.CASCADE, related_name='images')
    preview_image = models.URLField(blank=True, null=True)
    banner_image = models.URLField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    thumbnail_image = models.URLField(blank=True, null=True)

class HackathonMeta(models.Model):
    hackathon = models.OneToOneField('Hackathon', on_delete=models.CASCADE, related_name='meta')
    sponsor_logos = models.JSONField(null=True, blank=True)
    livestream_links = models.JSONField(null=True, blank=True)
    faq = models.JSONField(null=True, blank=True)

class HackathonStatistics(models.Model):
    hackathon = models.OneToOneField('Hackathon', on_delete=models.CASCADE, related_name='statistics')
    total_registered = models.PositiveIntegerField(default=0)
    total_submissions = models.PositiveIntegerField(default=0)
    total_teams = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)

class Hackathon(models.Model):
    STATUS_CHOICES = [
        ('anonce', 'Анонс'),
        ('start_registration', 'Регистрации'),
        ('end_registration', 'Регистрация завершена'),
        ('started', 'Проводится'),
        ('determining_stage', 'Определение победителей'),
        ('finished', 'Завершенный'),
    ]

    PARTICIPATION_TYPE_CHOICES = [
        ('solo', 'Индивидуальное'),
        ('team', 'Командное'),
        ('both', 'Оба варианта')
    ]

    name = models.CharField(max_length=100)
    short_description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, choices=[('online', 'Онлайн'), ('offline', 'Офлайн'), ('hybrid', 'Гибридный')], default='online')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='anonce')

    registration_limit = models.PositiveIntegerField(null=True, blank=True)
    allow_solo_registration = models.BooleanField(default=True)
    allow_team_registration = models.BooleanField(default=True)
    allow_team_search = models.BooleanField(default=True)

    participants = models.ManyToManyField(UserProfile, related_name='participated_hackathons')
    solo_participants = models.ManyToManyField(UserProfile, related_name='solo_hackathons', blank=True)
    tags = models.ManyToManyField('Tag', related_name='hackathons', blank=True)
    prize_pool = models.IntegerField(default=0)
    number_of_winners = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1)])
    max_team_size = models.PositiveIntegerField(default=4)
    
    organizer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='organized_hackathons')
    
    location = models.CharField(max_length=200, null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    program = models.TextField(null=True, blank=True)
    judges = models.TextField(null=True, blank=True)

    enable_public_voting = models.BooleanField(default=False)
    show_solutions_after_deadline = models.BooleanField(default=True)
    xp_reward_participation = models.PositiveIntegerField(default=50)
    xp_reward_winner = models.PositiveIntegerField(default=200)
    crystal_reward_winner = models.PositiveIntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
