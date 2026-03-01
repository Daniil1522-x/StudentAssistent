import calendar as cal_module
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Event


@login_required
def calendar(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    weeks = cal_module.monthcalendar(year, month)
    current = date(year, month, 1)

    events = Event.objects.filter(user=request.user, date__year=year, date__month=month)
    events_by_day = {}
    for event in events:
        events_by_day.setdefault(event.date.day, []).append(event)

    context = {
        'weeks': weeks,
        'month_name': current.strftime('%B %Y'),
        'today': today.day if (year == today.year and month == today.month) else -1,
        'prev_url': f'?year={prev_year}&month={prev_month}',
        'next_url': f'?year={next_year}&month={next_month}',
        'events_by_day': events_by_day,
        'year': year,
        'month': month,
        'important_dates': Event.objects.filter(user=request.user, event_type='important').order_by('date'),
        'session_periods': Event.objects.filter(user=request.user, event_type='session').order_by('date'),
        'rest_periods': Event.objects.filter(user=request.user, event_type='holiday').order_by('date'),
    }
    return render(request, 'calendar.html', context)


@login_required
def add_event(request):
    if request.method == 'POST':
        Event.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            date=request.POST.get('date'),
            description=request.POST.get('description', ''),
            event_type=request.POST.get('event_type', 'other'),
        )
        return redirect('calendar:calendar')
    selected_date = request.GET.get('date', '')
    return render(request, 'add_event.html', {'selected_date': selected_date})


@login_required
def delete_event(request, event_id):
    Event.objects.filter(id=event_id, user=request.user).delete()
    return redirect('calendar:calendar')