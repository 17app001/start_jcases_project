from cmath import log
from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.models import Profile, Respondent
from user.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from case.utils import get_page_object
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generator_token


@login_required(login_url='login')
def purchase(request):
    if request.method == 'POST':
        user = request.user
        purchase_point = eval(request.POST.get('purchase-select'))
        user.point += purchase_point
        user.save()

        return redirect('profile', id=user.id)

    return render(request, './user/purchase.html')

# 啟動玩家


@login_required(login_url='login')
def user_activate(requset, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Profile.objects.get(id=uid)

    except Exception as e:
        user = None

    # 檢查是否認證成功
    if user and generator_token.check_token(user, token):
        user.certification = True
        user.point += 100
        user.save()

    return redirect('profile', user.id)

# Create your views here.


@login_required(login_url='login')
def activate_email(request):
    user = request.user
    domain = get_current_site(request)
    try:
        email_subject = 'Activate your account'
        email_body = render_to_string('./user/activate.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': generator_token.make_token(user),
        })

        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )

        email.send()
        message = '認證EMAIL發送...'

    except Exception as e:
        print(e)
        message = '認證EMAIL發送失敗...'

    cases = user.case_set.all()
    page = request.GET.get('page')
    page_num = 10
    page_obj = get_page_object(cases, page, page_num)

    return render(request, './user/profile.html', {'user': user, 'message': message, 'page_obj': page_obj})


@login_required(login_url='login')
def update(request, id):
    respondents = Respondent.objects.all()
    user = Profile.objects.get(id=id)
    message = None

    if request.method == 'POST':
        new_email = request.POST.get('new-email')
        respondent_id = request.POST.get('respondent-id')

        # 已認證
        if user.certification:
            setattr(user, 'respondent', Respondent.objects.get(id=respondent_id))
            message = '資料更新成功!'
            user.save()

            return redirect('profile', id=user.id)

        elif not new_email:
            message = '請輸入Email'
        elif not Profile.objects.filter(email=new_email) or user.email == new_email:
            setattr(user, 'email', new_email)
            setattr(user, 'respondent', Respondent.objects.get(id=respondent_id))
            message = '資料更新成功!'
            user.save()

            return redirect('profile', id=user.id)
        else:
            message = 'Email已經註冊'

    return render(request, './user/update.html', {'message': message, 'respondents': respondents})


# 個人資訊
@login_required(login_url='login')
def profile(request, id):
    user = Profile.objects.get(id=id)
    cases = user.case_set.all()
    page = request.GET.get('page')
    page_num = 10
    page_obj = get_page_object(cases, page, page_num)

    respsone = render(request, './user/profile.html',
                      {'user': user, 'page_obj': page_obj})
    respsone.set_cookie('page', 'profile')

    return respsone


def user_register(request):
    form = ProfileForm()

    if request.method == 'POST':
        # 將資訊傳入
        form = ProfileForm(request.POST, request.FILES)
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
