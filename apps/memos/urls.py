from django.urls import path
from . import views

app_name = 'memos'

urlpatterns = [
    path('', views.memos, name='memos'),
    path('add/', views.add_memo, name='add_memo'),
    path('delete/<int:memo_id>/', views.delete_memo, name='delete_memo'),
]