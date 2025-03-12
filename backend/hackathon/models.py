from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Hackathon(models.Model):
    name = models.CharField(max_length=200)
    full_description = models.TextField()
    short_description = models.TextField()
    image = models.URLField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    participants = models.ManyToManyField(User, related_name='hackathons', blank=True)
    max_participants = models.PositiveIntegerField(default=100)
    prize_pool = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    is_online = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name='hackathons', blank=True)
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-start_date']

