from django.contrib import admin
from .models import UserProfile, Task, CustomTask, Moderator

admin.site.register(CustomTask)
admin.site.register(Moderator)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'exp_reward')
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
    list_display = ('user', 'level', 'exp')