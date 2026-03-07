from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('personal-info/', views.personal_info, name='personal_info'),
    path('update-personal-info/', views.update_personal_info, name='update_personal_info'),
]