from django.urls import path

from . import views

app_name = 'security'

urlpatterns = [
    path('passwords/', views.passwords, name='passwords'),
    path('passwords/add/', views.add_account, name='add_account'),
    path('passwords/<int:account_id>/delete/', views.delete_account, name='delete_account'),
    path('passwords/<int:account_id>/reveal/', views.reveal_password, name='reveal_password'),
    path('', views.security, name='security'),  # главная страница безопасности
]