from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            return render(request, 'users/registration.html', {'error_message': 'Пожалуйста, заполните все поля формы'})

        if User.objects.filter(username=username).exists():
            return render(request, 'users/registration.html', {'error_message': 'Пользователь с таким именем уже существует'})

        if not '@' in email:
            return render(request, 'users/registration.html', {'error_message': 'Пожалуйста, введите корректный email'})

        user = User.objects.create_user(username=username, email=email, password=make_password(password))
        user.save()
        login(request, user)
        return render(request, 'users/registration_success.html')

    return render(request, 'users/registration.html')


def myLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'main/index.html')
        else:
            error_message = "Неправильное имя пользователя или пароль"
            return render(request, 'users/login.html', {'error_message': error_message})
    else:
        return render(request, 'users/login.html')
    
def mylogout(request):
    logout(request) 
    return render(request, 'main/index.html') 

def success(request):
    return render(request, 'main/success.html') 

def privateOffice(request):
    return render(request, 'users/privateOffice.html') 

