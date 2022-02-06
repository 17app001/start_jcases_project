from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Case,Profile
from django.db.models import Count

# https://able.bio/rhett/how-to-order-by-count-of-a-foreignkey-field-in-django--26y1ug1
def get_top5_users():    
    users = Profile.objects.all().annotate(num_cases=Count('case')).order_by('-num_cases')[:5]
    
    return users


def get_top5_cases():
    cases = Case.objects.order_by('-view')[:5]

    return cases

# 搜尋cases
def search_cases(category_id, county_id, search=''):
    search_q = Q(title__contains=search) | Q(description__contains=search)
    category_q = Q(category_id=category_id)
    city_q = Q(owner__city_id=county_id)
    cases = None

    try:
        if category_id and county_id:
            cases = Case.objects.filter(category_q & city_q & search_q) if search else\
                Case.objects.filter(category_q & city_q)
        elif category_id:
            cases = Case.objects.filter(
                category_q & search_q) if search else\
                Case.objects.filter(category_q)
        elif county_id:
            cases = Case.objects.filter(city_q & search_q) if search else\
                Case.objects.filter(city_q)
        elif search:
            cases = Case.objects.filter(search_q)
        else:
            cases = Case.objects.all()
    except Exception as e:
        print(e)

    return cases


def get_page_object(cases, page, page_num):
    # 每次固定顯示幾筆資料
    paginator = Paginator(cases, page_num)
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return page_obj
