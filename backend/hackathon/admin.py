from django.contrib import admin
from .models import Hackathon, HackathonImages, HackathonMeta, HackathonStatistics, HackathonTime


# Inline для изображений
class HackathonImagesInline(admin.StackedInline):
    model = HackathonImages
    extra = 0  # Убирает пустые дополнительные поля
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"
    fk_name = 'hackathon'


# Inline для мета-информации
class HackathonMetaInline(admin.StackedInline):
    model = HackathonMeta
    extra = 0
    verbose_name = "Мета-информация"
    verbose_name_plural = "Мета-информация"
    fk_name = 'hackathon'


# Inline для статистики
class HackathonStatisticsInline(admin.StackedInline):
    model = HackathonStatistics
    extra = 0
    verbose_name = "Статистика"
    verbose_name_plural = "Статистика"
    fk_name = 'hackathon'


# Inline для времени проведения
class HackathonTimeInline(admin.StackedInline):
    model = HackathonTime
    extra = 0
    verbose_name = "Время проведения"
    verbose_name_plural = "Время проведения"
    fk_name = 'hackathon'


# Основной админ для Hackathon
@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    search_fields = ('name', 'full_description', 'short_description', 'tags')
    list_filter = ('status', 'type')
    inlines = [
        HackathonImagesInline,
        HackathonMetaInline,
        HackathonStatisticsInline,
        HackathonTimeInline,
    ]
    fieldsets = (
        (None, {
            'fields': ('name', 'full_description', 'short_description', 'type', 'status')
        }),
        ('Регистрация', {
            'fields': ('registration_limit', 'allow_solo_registration', 'allow_team_registration', 'allow_team_search')
        }),
        ('Награды и участие', {
            'fields': ('prize_pool', 'number_of_winners', 'max_team_size')
        }),
        ('Организатор и настройки', {
            'fields': ('organizer', 'enable_public_voting', 'show_solutions_after_deadline',
                       'xp_reward_participation', 'xp_reward_winner', 'crystal_reward_winner')
        }),
    )
