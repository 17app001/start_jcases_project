from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Case
from .forms import CreateCaseForm
from datetime import datetime
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
    cases = Case.objects.all()
    # print(cases)
    return render(request, './case/cases.html', {'cases': cases})
