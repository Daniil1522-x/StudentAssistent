# apps/accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Личная информация (просмотр профиля)
    path('personal-info/', views.personal_info, name='personal_info'),

    # Обновление личной информации (форма сохранения)
    path('update-personal-info/', views.update_personal_info, name='update_personal_info'),

    # Если позже добавишь аутентификацию / мастер-пароль
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    # path('master-password/', views.master_password_check, name='master_password_check'),
    # path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('personal-info/', views.personal_info, name='personal_info'),
    path('update-personal-info/', views.update_personal_info, name='update_personal_info'),
]