from django.urls import path

from .views import add_discipline, disciplines

app_name = 'disciplines'

urlpatterns = [
    path('', disciplines, name='disciplines'),
    path('add/', add_discipline, name='add_discipline'),
]