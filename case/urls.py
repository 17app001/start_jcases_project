from django.urls import path
from . import views

urlpatterns = [
    # 設定成首頁
    path('', views.cases, name='cases'),
    path('case/<str:id>', views.case, name='case'),
    path('create-case/', views.create_case, name='create-case'),
]
