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
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.db.models import Sum


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
            # Jangan buat UserProfile manual jika signal sudah ada
            messages.success(request, "Akun berhasil dibuat! Silakan login.")
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
    
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "Profil tidak ditemukan, silakan registrasi ulang.")
        return redirect('register')
    return render(request, 'index.html', {'user_profile': user_profile})

    # Menambahkan top_players untuk leaderboard
    top_players = UserProfile.objects.select_related('user').order_by('-exp')[:5]

    return render(request, 'index.html', {'user_profile': user_profile, 'top_players': top_players})



def user_logout(request):
    logout(request)
    return redirect('login')

@csrf_exempt 
def complete_task(request, task_id):
    try:
        # Cek apakah task merupakan DailyTask atau CustomTask
        task = DailyTask.objects.get(id=task_id)
        
        if task.is_completed:
            messages.warning(request, "Tugas ini sudah selesai sebelumnya.")
            return redirect('task_list')

        # Tandai sebagai selesai
        task.is_completed = True    
        task.save()

        # Update EXP dan Coins hanya jika DailyTask
        user_profile = task.user
        user_profile.add_exp(task.task.exp_reward)
        user_profile.add_coins(task.task.coin_reward)
        user_profile.save()
        messages.success(request, f"Tugas '{task.task.title}' selesai! Kamu mendapatkan {task.task.exp_reward} EXP dan {task.task.coin_reward} koin!")
    except DailyTask.DoesNotExist:
        try:
            # Jika bukan DailyTask, cek CustomTask
            task = CustomTask.objects.get(id=task_id)
            task.is_completed = True
            task.save()
            messages.success(request, f"Tugas custom '{task.title}' berhasil diselesaikan!")
        except CustomTask.DoesNotExist:
            messages.error(request, "Tugas tidak ditemukan.")
     
    return redirect('task_list')


def task_list(request):
    difficulty_filter = request.GET.get('difficulty', None)
    tasks = Task.objects.all().order_by('-id')
    custom_tasks = CustomTask.objects.filter(user=request.user.userprofile).order_by('-id')
    if difficulty_filter:
        tasks = tasks.filter(difficulty=difficulty_filter)

    #      # Perbaikan: Gabungkan tasks dan custom_tasks untuk ditampilkan bersama
    # all_tasks = list(tasks) + list(custom_tasks)
    # return render(request, 'task_list.html', {'tasks': tasks, 'custom_tasks': custom_tasks})

# Mengirimkan hanya tugas yang sudah dihubungkan dengan DailyTask
    custom_tasks = CustomTask.objects.filter(user=request.user.userprofile).order_by('-id')
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
    today = now().date()
    # Filter user dengan exp yang bertambah dalam 7 hari terakhir
    top_users = UserProfile.objects.annotate(
        total_exp=Sum('exp')
    ).order_by('-exp')[:5]

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


    