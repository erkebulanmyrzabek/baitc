from django.db import models

# Create your models here.
class Hackathon(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    registration_deadline = models.DateField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-created_at']

class Webinar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    speaker = models.CharField(max_length=255)
    date = models.DateTimeField()
    duration = models.DurationField()  # Длительность в минутах
    link = models.URLField(blank=True, null=True)  # Ссылка на вебинар
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class CaseCup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)  # Компания, проводящая кейс-чемпионат
    prize_fund = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_deadline = models.DateField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']
