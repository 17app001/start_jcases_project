from cmath import log
from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from user.models import Profile
from user.forms import ProfileForm


# Create your views here.

# 註冊


def user_register(request):
    form = ProfileForm()
    if request.method == 'POST':
        # 將資訊傳入
        form = ProfileForm(request.POST)
        print(form)
        # 表單輸入是否正確
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)

            return redirect('cases')

    return render(request, './user/register.html', {'form': form})

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
