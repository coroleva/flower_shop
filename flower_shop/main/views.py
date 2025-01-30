

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm

from django.contrib.auth import logout
from django.shortcuts import redirect

def index(request):
    data = {
        'caption': 'Магазин цветов'
    }
    return render(request,  'main/index.html', data) # возвращаем html-файл на главную страницу

def new(request):
    return render(request,  'main/new.html')


# C:\Users\User\Documents\GitHub\flower\flower_shop\templates\main\index.html



def logout_view(request):
    logout(request)
    return redirect('catalog:catalog')  # Перенаправляем на каталог или главную страницу



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматическая авторизация
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('catalog')  # Перенаправление на страницу каталога
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})