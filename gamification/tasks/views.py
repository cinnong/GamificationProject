from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Task, DailyTask, CustomTask, UserProfile, Achievement, UserAchievement, Notification
from .serializers import TaskSerializer, UserProfileSerializer
from .forms import CustomTaskForm, UserRegisterForm, UserLoginForm
from django.contrib.auth.views import LoginView
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user)
            task = Task.objects.first()
            DailyTask.objects.create(user=user_profile, task=task, day=date.today())
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = UserLoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Username atau password salah!")
    return render(request, 'login.html', {'form':form})

@login_required
def index(request):
    return render(request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def complete_task(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id)
    if task.is_completed:
        messages.warning(request, "Tugas ini sudah diselesaikan sebelumnya.")
        return redirect('task_list')
    task.is_completed = True
    task.save()
    try:
        user_profile = UserProfile.objects.get(user=task.user.user)
        user_profile.add_exp(task.task.exp_reward)
        user_profile.add_coins(task.task.coin_reward)
    except UserProfile.DoesNotExist:
        messages.error(request, "Profil pengguna tidak ditemukan.")
        return redirect('task_list')
    messages.success(
        request,
        f"Tugas '{task.task.title}' selesai! Kamu mendapatkan {task.task.exp_reward} EXP dan {task.task.coin_reward} koin!"
    )
    return redirect('task_list')

def task_list(request):
    difficulty_filter = request.GET.get('difficulty', None)
    tasks = Task.objects.all().order_by('-id')
    custom_tasks = CustomTask.objects.filter(user=request.user.userprofile).order_by('-id')
    if difficulty_filter:
        tasks = tasks.filter(difficulty=difficulty_filter)
    return render(request, 'task_list.html', {'tasks': tasks, 'custom_tasks': custom_tasks})

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
    return render(request, 'custom_tasks.html', {'form': form})

def delete_custom_task(request, task_id):
    task = get_object_or_404(CustomTask, id=task_id)
    task.delete()
    return redirect('task_list')

def leaderboard(request):
    top_users = UserProfile.objects.order_by('-exp')[:10]
    return render(request, 'tasks/leaderboard.html', {'top_users': top_users})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile.html', {'profile': profile, 'form': form})