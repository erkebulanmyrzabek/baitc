from django.db import models
from django.contrib.auth.models import User

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/')
    
    def __str__(self):
        return self.name

class TechStack(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='tech_stack/')
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    telegram_id = models.CharField(max_length=100, unique=True)
    achievements = models.ManyToManyField(Achievement, through='UserAchievement')
    tech_stack = models.ManyToManyField(TechStack, through='UserTechStack')
    
    def __str__(self):
        return f"Profile of {self.user.username}"

class UserAchievement(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)
    unlocked_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user_profile', 'achievement')

class UserTechStack(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tech = models.ForeignKey(TechStack, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)  # 0-100
    
    class Meta:
        unique_together = ('user_profile', 'tech')
