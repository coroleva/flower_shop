
from django.urls import path
from . import views
from .views import logout_view
from django.urls import path
from .views import register

from django.urls import path
from .views import register  # Импортируем представление регистрации
from django.contrib.auth import views as auth_views  # Встроенные представления Django
urlpatterns = [
    path('', views.index, name='index'), # главная страница
    path('new/', views.new, name='new'), # страница о нас
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]