from django.contrib import admin
from .models import UserProfile, Task, WeeklyTask, DailyTask, CustomTask, Item, UserItem, Moderator, Notification, Achievement, UserAchievement

admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(WeeklyTask)
admin.site.register(DailyTask)
admin.site.register(CustomTask)
admin.site.register(Item)
admin.site.register(UserItem)
admin.site.register(Moderator)
admin.site.register(Notification)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
# Register your models here.
