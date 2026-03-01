# apps/connections/urls.py
from django.urls import path
from . import views

app_name = 'connections'

urlpatterns = [
    path('', views.connections, name='connections'),
    path('add/', views.add_connection, name='add_connection'),
]
    # если добавишь форму
    # path('add/', views.add_connection, name='add_connection'),
