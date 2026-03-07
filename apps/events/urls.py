# apps/events/urls.py
from django.urls import path
from . import views


app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.home, name='index'),

]