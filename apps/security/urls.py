from django.urls import path
from . import views

app_name = 'security'

urlpatterns = [
    path('passwords/', views.passwords, name='passwords'),
    path('passwords/add/', views.add_account, name='add_account'),
    path('', views.security, name='security'),  # главная страница безопасности
]