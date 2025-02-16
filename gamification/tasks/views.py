from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Task, CustomTask, UserProfile, UserTaskCompletion, UserCustomTaskCompletion
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
from django.utils import timezone
from django.db import models


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
        userprofile = request.user
    except UserProfile.DoesNotExist:
        messages.error(request, "Profil tidak ditemukan, silakan registrasi ulang.")
        return redirect('register')
    return render(request, 'index.html', {'user': userprofile})



def user_logout(request):
    logout(request)
    return redirect('login')

@csrf_exempt
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user_profile = request.user.userprofile

    # Check if the task has already been completed by the user
    if UserTaskCompletion.objects.filter(user=user_profile, task=task).exists():
        messages.warning(request, "Tugas ini sudah selesai sebelumnya.")
        return redirect('task_list')

    # Mark the task as completed for the user
    UserTaskCompletion.objects.create(user=user_profile, task=task)
    user_profile.add_exp(task.exp_reward)
    user_profile.save()
    messages.success(request, f"Tugas '{task.title}' selesai! Kamu mendapatkan {task.exp_reward} EXP!")

    return redirect('task_list')


from .models import Task, CustomTask, UserProfile
import random

@login_required
def task_list(request):
    difficulty_filter = request.GET.get('difficulty', None)
    user_profile = request.user.userprofile

    easy_tasks = list(Task.objects.filter(difficulty='easy').order_by('created_at')[:2])
    medium_tasks = list(Task.objects.filter(difficulty='medium').order_by('created_at')[:2])
    hard_tasks = list(Task.objects.filter(difficulty='hard').order_by('created_at')[:1])
    
    tasks = easy_tasks + medium_tasks + hard_tasks
    random.shuffle(tasks)
    
    tasks = Task.objects.all().distinct()
    custom_tasks = CustomTask.objects.filter(user=user_profile).distinct()

    if difficulty_filter:
        tasks = tasks.filter(difficulty=difficulty_filter)
        
    completed_tasks = UserTaskCompletion.objects.filter(user=user_profile).values_list('task_id', flat=True)

    # Send the choices from Task model
    difficulty_choices = Task.DIFFICULTY_CHOICES
    
    return render(request, 'task_list.html', {
        'tasks': tasks,
        'custom_tasks': custom_tasks,
        'difficulty_choices': difficulty_choices,
        'completed_tasks': completed_tasks
    })

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

@csrf_exempt
@login_required
def complete_custom_task(request, task_id):
    custom_task = get_object_or_404(CustomTask, id=task_id)
    user_profile = request.user.userprofile

    # Check if the custom task has been validated
    if not custom_task.is_validated:
        messages.warning(request, "Tugas custom ini belum divalidasi oleh moderator.")
        return redirect('task_list')

    # Check if the custom task has already been completed by the user
    if UserCustomTaskCompletion.objects.filter(user=user_profile, task=custom_task).exists():
        messages.warning(request, "Tugas custom ini sudah selesai sebelumnya.")
        return redirect('task_list')

    # Mark the custom task as completed for the user
    UserCustomTaskCompletion.objects.create(user=user_profile, task=custom_task)
    custom_task.is_completed = True
    custom_task.save()
    user_profile.add_exp(custom_task.exp_reward)
    user_profile.save()
    messages.success(request, f"Tugas custom '{custom_task.title}' selesai! Kamu mendapatkan {custom_task.exp_reward} EXP!")

    # Schedule the custom task for deletion after 12 hours
    custom_task.schedule_deletion()

    return redirect('task_list')

@login_required
def leaderboard(request):
    # Fetch users ordered by level, exp, and finished task time
    users = UserProfile.objects.annotate(
        last_task_time=models.Max('usertaskcompletion__completed_at')
    ).order_by('-level', '-exp', 'last_task_time')[:10]

    return render(request, 'leaderboard.html', {'users': users})


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


    