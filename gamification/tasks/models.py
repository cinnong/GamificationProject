from django.db import models
from django.contrib.auth.models import User 
from django_resized import ResizedImageField
from tinymce.models import HTMLField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)  # Kolom bio ditambahkan
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    exp_reward = models.IntegerField()
    coin_reward = models.IntegerField()

    def __str__(self):
        return self.title

class DailyTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    day = models.DateField()
    is_completed = models.BooleanField(default=False)
from django.db import models


class CustomTask(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('tasks.UserProfile', on_delete=models.CASCADE)
    description = models.TextField()
    exp_reward = models.IntegerField()
    coin_reward = models.IntegerField()
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    level_requirement = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class UserItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.user.username} - {self.item.name}"

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user.username} - {self.message}"
    
class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    exp_reward = models.IntegerField()

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.achievement.name}"


