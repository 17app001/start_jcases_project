from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Case
from .forms import CreateCaseForm
# Create your views here.


def case(request, id):
    case = Case.objects.get(id=id)

    case.view += 1
    setattr(case, 'view', case.view)
    case.save()

    return render(request, './case/case.html', {'case': case})


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

            return redirect('cases')

    return render(request, './case/create-case.html', {'form': form})


def cases(request):
    cases = Case.objects.all()
    # print(cases)
    return render(request, './case/cases.html', {'cases': cases})
