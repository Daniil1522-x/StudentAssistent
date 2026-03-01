from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Connection


@login_required
def connections(request):
    user_connections = Connection.objects.filter(user=request.user)

    # Группируем по категориям
    grouped = {}
    for conn in user_connections:
        grouped.setdefault(conn.category, []).append(conn.text)

    return render(request, 'connections.html', {'connections': grouped})


@login_required
def add_connection(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        text = request.POST.get('text')
        if category and text:
            Connection.objects.create(user=request.user, category=category, text=text)
        return redirect('connections:connections')
    return render(request, 'add_connection.html', {})