from django.urls import path
from . import views

urlpatterns = [
    # 設定成首頁
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/<str:id>', views.profile, name='profile'),
    path('update/<str:id>',views.update,name='update'),
    path('activate-email/', views.activate_email,name='activate-email'),
      path('activate-user/<uidb64>/<token>/',views.user_activate, name='activate'),
]
