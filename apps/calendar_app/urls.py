from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.calendar, name='calendar'),
    path('add/', views.add_event, name='add_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]