# apps/events/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import generate_calendar_data


@login_required
def home(request):
    # user_profile = request.user.profile  # если есть модель Profile
    context = {
        # 'user': user_profile,
        'calendar': generate_calendar_data(),  # теперь функция доступна
        'upcoming_events': [],  # пока пусто
    }
    return render(request, 'index.html', context)