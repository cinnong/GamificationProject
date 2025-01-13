from django.contrib import admin
from .models import UserProfile, Task, DailyTask, CustomTask, Item, UserItem, Moderator, Notification, Achievement, UserAchievement

# admin.site.register(UserProfile)
# admin.site.register(Task)
admin.site.register(DailyTask)
admin.site.register(CustomTask)
admin.site.register(Item)
admin.site.register(UserItem)
admin.site.register(Moderator)
admin.site.register(Notification)
admin.site.register(Achievement)
admin.site.register(UserAchievement)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'exp_reward', 'coin_reward')
    list_filter = ('difficulty',)
    search_fields = ('title', 'description')
    ordering = ('difficulty',)

    # Validasi dengan choices dropdown langsung di admin panel
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['difficulty'].choices = Task.DIFFICULTY_CHOICES
        return form

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'exp', 'coins')