# apps/university/urls.py
from django.urls import path
from . import views

app_name = 'university'

urlpatterns = [
    path('', views.university_info, name='university_info'),
]