from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('tasks/delete/<int:task_id>/', views.delete_custom_task, name='delete_custom_task'),
    path('create/', views.create_custom_task, name='create_custom_task'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
