from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tables import Description
from .models import Case, Category
from .forms import CreateCaseForm
from user.models import City
from datetime import datetime
from django.db.models import Q
# Create your views here.


@login_required(login_url='login')
def update_case(request, id):
    case = Case.objects.get(id=id)
    page = request.COOKIES.get('page')

    if request.method == 'POST':
        case.updatedon = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form = CreateCaseForm(request.POST, instance=case)

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
    setattr(case, 'view', case.view)
    case.save()

    respsone = render(request, './case/case.html', {'case': case})
    respsone.set_cookie('page', 'case')

    return respsone


@login_required(login_url='login')
def create_case(request):
    # GET情況
    form = CreateCaseForm()

    if request.method == 'POST':
        form = CreateCaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            # 設定擁有者
            case.owner = request.user
            case.save()
            form.save_m2m()

            return redirect('cases')

    return render(request, './case/create-case.html', {'form': form})


def cases(request):
   
    categorys = Category.objects.all()
    countys = City.objects.all()

    category_id, county_id = 0, 0
    search = ''

    if request.method=='GET':      
        cases = Case.objects.all()

    if request.method == 'POST':
        category_id = eval(
            request.POST['category']) if request.POST['category'] else 0
        county_id = eval(request.POST['county']
                         ) if request.POST['county'] else 0
        search = request.POST['search']
        try:
            if category_id and county_id:
                if search:
                     cases = Case.objects.filter(Q(category_id=category_id) & Q(
                    owner__city_id=county_id)).filter(
                    Q(title__contains=search) | Q(description__contains=search))
                else:
                    cases = Case.objects.filter(Q(category_id=category_id) & Q(
                        owner__city_id=county_id))                    
            elif category_id:
                if search:
                    cases = Case.objects.filter(category_id=category_id).filter(
                    Q(title__contains=search) | Q(description__contains=search))
                else:
                    cases = Case.objects.filter(category_id=category_id)
            elif county_id:
                if search:
                     cases = Case.objects.filter(owner__city_id=county_id).filter(
                    Q(title__contains=search) | Q(description__contains=search))
                cases = Case.objects.filter(owner__city_id=county_id)
            elif search:
                    cases = Case.objects.filter(
                     Q(title__contains=search) | Q(description__contains=search))   
            else:
                cases = Case.objects.all()
         

        except Exception as e:
            print(e)    

    context = {'cases': cases, 'categorys': categorys, 'countys': countys, 'search': search,
               'category_id': category_id, 'county_id': county_id}

    return render(request, './case/cases.html', context=context)
