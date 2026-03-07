from django.urls import path
from . import views

app_name = 'sources'

urlpatterns = [
    path('', views.sources, name='sources'),
]