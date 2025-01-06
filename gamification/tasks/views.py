from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework import viewsets
from .models import Task, DailyTask, CustomTask, UserProfile, Achievement, UserAchievement, Notification
from .serializers import TaskSerializer, UserProfileSerializer
from .forms import CustomTaskForm, UserRegisterForm, UserLoginForm

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

def check_achievements(user):
    achievements = Achievement.objects.all()
    for achievement in achievements:
        if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            # Check if user meets the criteria for the achievement
            # If yes, create UserAchievement and reward user
            pass

def complete_task(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id)
    task.is_completed = True
    task.save()
    Notification.objects.create(user=task.weekly_task.user, message=f"Task '{task.weekly_task.task.title}' completed!")
    return redirect('task_list')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def complete_task(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id)
    task.is_completed = True
    task.save()
    return redirect('task_list')

def create_custom_task(request):
    if request.method == 'POST':
        form = CustomTaskForm(request.POST)
        if form.is_valid():
            custom_task = form.save(commit=False)
            custom_task.user = request.user.userprofile
            custom_task.save()
            return redirect('task_list')
    else:
        form = CustomTaskForm()
    return render(request, 'tasks/create_custom_task.html', {'form': form})

def leaderboard(request):
    top_users = UserProfile.objects.order_by('-exp')[:10]
    return render(request, 'tasks/leaderboard.html', {'top_users': top_users})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserRegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = UserLoginForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

# Create your views here.
