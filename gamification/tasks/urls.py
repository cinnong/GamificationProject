from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('', views.task_list, name='task_list'),
    path('create/', views.create_custom_task, name='create_custom_task'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('profile/', views.profile_view, name='profile'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]


