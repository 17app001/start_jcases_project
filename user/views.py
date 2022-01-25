from cmath import log
from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.models import Profile,City,Respondent
from user.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from case.models import Case
from case.utils import get_page_object

# Create your views here.

@login_required(login_url='login')
def user_update(request,id):   
    respondents=Respondent.objects.all()
    user = Profile.objects.get(id=id)
    message=None

    if request.method=='POST':       
        new_email=request.POST.get('new-email')       
        respondent_id=request.POST.get('respondent-id')       

        if not new_email:
            message='請輸入Email'                 
        elif not Profile.objects.filter(email=new_email) or user.email==new_email:
            setattr(user, 'email', new_email)          
            setattr(user,'respondent',Respondent.objects.get(id=respondent_id))
            message='資料更新成功!'           
            user.save()

            return redirect('profile', id=user.id)
        else:         
            message='Email已經註冊'            

        
    return render(request, './user/update.html',{'message':message,'respondents':respondents})


# 個人資訊
@login_required(login_url='login')
def profile(request, id):
    user = Profile.objects.get(id=id)
    cases=user.case_set.all()
    page = request.GET.get('page')
    page_num=10
    page_obj = get_page_object(cases, page, page_num)

    respsone=render(request, './user/profile.html', {'user': user,'page_obj':page_obj})
    respsone.set_cookie('page','profile') 

    return respsone


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

            return redirect('index')

    return render(request, './user/register.html', {'form': form})

# 登出


@login_required(login_url='login')
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
                return redirect('index')
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
