from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('reset-password/',auth_views.PasswordResetView.as_view(
        template_name='./user/reset-password.html'),name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='./user/reset-password-confirm.html'),
        name='password_reset_confirm'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(
        template_name='./user/reset-password-send.html'),
        name='password_reset_done'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='./user/reset-password-complete.html'),
        name='password_reset_complete'),

    # 設定成首頁
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/<str:id>', views.profile, name='profile'),
    path('update/<str:id>',views.update,name='update'),    
    path('activate-email/', views.activate_email,name='activate-email'),
    path('activate-user/<uidb64>/<token>/',views.user_activate, name='activate'),

  
]
