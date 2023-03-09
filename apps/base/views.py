from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        user = User.objects.filter(username=username)
        if user.exists():
            messages.warning(request, "User already exists!")
            return redirect('register')
        else:
            if password1 == password2:
                instance = User.objects.create_user(username=username, password=password1)
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                messages.success(request, 'Your account has been created!')
                return redirect('/')
            else:
                messages.warning(request, "Passwords do not match")
                return redirect('register')
    return render(request, "register.html")


def login_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Phone number or Password is incorrect")
            return HttpResponseRedirect('/login')

    return render(request, "login.html")


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')
