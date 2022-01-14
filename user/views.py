from cmath import log
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from user.models import Profile

# Create your views here.

# 登出


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')


# 登入
def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('cases')
            else:
                if Profile.objects.filter(username=username).exists():
                    message = '密碼錯誤'
                else:
                    message = '帳號錯誤'

                print(message)

        except Exception as e:
            print(e)

        return render(request, './user/login.html', {'username': username, 'password': password, 'message': message})

    return render(request, './user/login.html')
