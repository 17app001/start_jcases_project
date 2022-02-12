
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Case, Category
from .forms import CreateCaseForm
from user.models import City
from datetime import datetime
from .utils import search_cases, get_page_object, get_top5_cases, get_top5_users
from django.core.files.storage import FileSystemStorage


@login_required(login_url='login')
def update_case(request, id):
    case = Case.objects.get(id=id)
    page = request.COOKIES.get('page')

    if request.method == 'POST':
        case.updatedon = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form = CreateCaseForm(request.POST,request.FILES, instance=case)

        if form.is_valid():
            form.save()

            if page == 'case':
                return redirect('case', id=case.id)

            return redirect('profile', id=request.user.id)

    if request.method == 'GET':
        form = CreateCaseForm(instance=case)

    return render(request, './case/update-case.html', {'form': form, 'page': page})


@login_required(login_url='login')
def delete_case(request, id):
    case = Case.objects.get(id=id)
    page = request.COOKIES.get('page')

    if request.method == 'POST':
        if request.POST.get('confirm'):
            case.delete()
            if page == 'case':
                return redirect('cases')

            return redirect('profile', id=request.user.id)

        elif request.POST.get('cancel'):
            if page == 'case':
                return redirect('case', id=case.id)

            return redirect('profile', id=request.user.id)

    return render(request, './case/delete-case.html', {'case': case})


def case(request, id):
    case = Case.objects.get(id=id)
    case.view += 1
    case.save()

    respsone = render(request, './case/case.html', {'case': case})
    respsone.set_cookie('page', 'case')

    return respsone


@login_required(login_url='login')
def create_case(request):
    # GET情況
    form = CreateCaseForm()

    if request.method == 'POST':
        form = CreateCaseForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            # 設定擁有者
            case.owner = request.user
            case.owner.point -= 1
            case.owner.save()
            case.save()
            form.save_m2m()

            return redirect('cases')

    return render(request, './case/create-case.html', {'form': form})


def index(request):
    category_id, county_id, search = 0, 0, ''
    page_num = 20
    page = request.GET.get('page')

    categorys = Category.objects.all()
    countys = City.objects.all()
    cases = search_cases(category_id, county_id, search)
    page_obj = get_page_object(cases, page, page_num)
    top5_cases = get_top5_cases()
    top5_users = get_top5_users()

    context = {'categorys': categorys, 'countys': countys, 'search': search,
               'category_id': category_id, 'county_id': county_id, 'page_obj': page_obj,
               'top5_cases': top5_cases, 'top5_users': top5_users, 'cases_length': len(cases)}

    response = render(request, './case/cases.html', context=context)
    # 刪除cookie
    response.delete_cookie('category_id')
    response.delete_cookie('county_id')
    response.delete_cookie('search')

    return response


def cases(request):
    categorys = Category.objects.all()
    countys = City.objects.all()
    top5_cases = get_top5_cases()
    top5_users = get_top5_users()
    # 取得cookies
    category_id = request.COOKIES.get('category_id', 0)
    county_id = request.COOKIES.get('county_id', 0)
    search = request.COOKIES.get('search', '')
    # 轉型成數值進行搜尋用
    category_id = eval(category_id) if type(
        category_id) == str else category_id
    county_id = eval(county_id) if type(county_id) == str else county_id

    if request.method == 'GET':
        page = request.GET.get('page')
        cases = search_cases(category_id, county_id, search)

    if request.method == 'POST':
        # 重新取得頁數
        page = 1
        category_id = eval(
            request.POST['category']) if request.POST['category'] else 0
        county_id = eval(request.POST['county']
                         ) if request.POST['county'] else 0
        search = request.POST['search']
        cases = search_cases(category_id, county_id, search)

    page_num = 20
    page_obj = get_page_object(cases, page, page_num)

    context = {'categorys': categorys, 'countys': countys, 'search': search,
               'category_id': category_id, 'county_id': county_id, 'page_obj': page_obj,
               'top5_cases': top5_cases, 'top5_users': top5_users, 'cases_length': len(cases)}

    response = render(request, './case/cases.html', context=context)

    # post 才會更新搜尋需求
    if request.method == 'POST':
        # 儲存為字串
        response.set_cookie('category_id', category_id)
        response.set_cookie('county_id', county_id)
        # 設定中文
        response.set_cookie('search', bytes(
            search, 'utf-8').decode('iso-8859-1'))

    return response
