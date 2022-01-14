from cmath import log
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

        print(username, password)

        try:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)

                return redirect('cases')
            else:
                print('登入失敗!')

        except Exception as e:
            print(e)

    return render(request, './user/login.html')
