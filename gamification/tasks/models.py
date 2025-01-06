from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from tinymce.models import HTMLField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True, null=False)
    bio = HTMLField(null=True, blank=True)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default=None, null=True, blank=True)
    exp = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

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

class WeeklyTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    week_start_date = models.DateField()

    def __str__(self):
        return f"{self.user.user.username} - {self.task.title} - {self.week_start_date}"

class DailyTask(models.Model):
    weekly_task = models.ForeignKey(WeeklyTask, on_delete=models.CASCADE)
    day = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.weekly_task.user.user.username} - {self.weekly_task.task.title} - {self.day}"

class CustomTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    exp_reward = models.IntegerField()
    coin_reward = models.IntegerField()
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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
# Create your models here.
