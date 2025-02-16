from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    profile_picture = ResizedImageField(size=[50, 80], quality=100, upload_to="profile_pics", default=None, null=True, blank=True)
    banner_image = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    
    def calculate_exp_to_level(self):
        return 100 + (self.level - 1) * 50  # Example: Increase by 50 EXP per level

    def add_exp(self, exp):
        self.exp += exp
        while self.exp >= self.calculate_exp_to_level():
            self.exp -= self.calculate_exp_to_level()
            self.level += 1
        self.save()
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    exp_reward = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reset = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def reset_task(self):
        self.is_completed = False
        self.last_reset = timezone.now()
        self.save()
        
class UserTaskCompletion(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

class CustomTask(models.Model):
    EXP_CHOICES = [
        (0, '0 EXP'),
        (50, '50 EXP'),
        (75, '75 EXP'),
        (100, '100 EXP'),
    ]
    
    title = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()
    exp_reward = models.IntegerField(default=0, choices=EXP_CHOICES)
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def schedule_deletion(self):
        deletion_time = timezone.now() + timedelta(hours=12)
        self.delete_at = deletion_time
        self.save()

class UserCustomTaskCompletion(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(CustomTask, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username