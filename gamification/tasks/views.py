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
from .models import DailyTask, Notification, UserProfile
    


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'  # Path ke template login yang benar

def index(request):
    return render(request, 'index.html')

def check_achievements(user):
    achievements = Achievement.objects.all()
    for achievement in achievements:
        if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            # Check if user meets the criteria for the achievement
            # If yes, create UserAchievement and reward user
            pass

from django.contrib import messages

def complete_task(request, task_id):
    try:
        task = DailyTask.objects.get(id=task_id)
    except DailyTask.DoesNotExist:
        messages.error(request, "Tugas tidak ditemukan!")
        return redirect('task_list')

    if task.is_completed:
        messages.warning(request, "Tugas ini sudah diselesaikan sebelumnya.")
        return redirect('task_list')

    # Tandai sebagai selesai
    task.is_completed = True
    task.save()

    # Update EXP dan koin pengguna setelah menyelesaikan tugas
    user_profile = task.user
    user_profile.exp += task.task.exp_reward
    # Tambahkan coins jika atribut sudah ada
    if hasattr(user_profile, 'coins'):
        user_profile.coins += task.task.coin_reward
    user_profile.save()

    # Tambahkan notifikasi dengan messages
    messages.success(
        request,
        f"Tugas '{task.task.title}' selesai! Kamu mendapatkan {task.task.exp_reward} EXP dan {task.task.coin_reward} koin!"
    )
    
    return redirect('task_list')


def task_list(request):
    difficulty_filter = request.GET.get('difficulty', None)
    tasks = Task.objects.all()
    
    if difficulty_filter:
        tasks = tasks.filter(difficulty=difficulty_filter)

    return render(request, 'task_list.html', {'tasks': tasks})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Membuat profil dan daily task otomatis saat register
            user_profile = UserProfile.objects.create(user=user)

            # Buat DailyTask otomatis saat register
            task = Task.objects.first()  # Ambil task pertama sebagai contoh
            DailyTask.objects.create(user=user_profile, task=task, day=date.today())

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

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
            # Membuat user profile otomatis
            UserProfile.objects.create(user=user)
            # Redirect ke halaman login setelah sukses register
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Cek apakah UserProfile sudah ada, jika belum buat
                if not UserProfile.objects.filter(user=user).exists():
                    UserProfile.objects.create(user=user)
                login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

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

def user_logout(request):
    logout(request)
    return redirect('login')


