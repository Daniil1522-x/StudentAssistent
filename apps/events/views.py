from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import generate_calendar_data


@login_required
def home(request):
    context = {
        'calendar': generate_calendar_data(),
        'upcoming_events': [],
    }
    return render(request, 'index.html', context)