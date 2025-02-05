"""
URL configuration for gamification project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, UserProfileViewSet, index
from tasks import views  # Import views secara langsung
from tasks.views import profile_view
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),   # Redirect setelah login
    path('tasks/', include('tasks.urls')),  
    path('profile/', profile_view, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    
    path('api/', include('rest_framework.urls')),  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)