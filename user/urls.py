from django.urls import path
from . import views

urlpatterns = [
    # 設定成首頁
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('update/<str:id>',views.user_update,name='update'),
    path('profile/<str:id>', views.profile, name='profile'),  
]
