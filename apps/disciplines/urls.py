from django.urls import path
from .views import disciplines, add_discipline

app_name = 'disciplines'

urlpatterns = [
    path('', disciplines, name='disciplines'),
    path('add/', add_discipline, name='add_discipline'),
]