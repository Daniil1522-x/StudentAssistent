from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ConnectionForm
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
        form = ConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.user = request.user
            connection.save()
            return redirect('connections:connections')
        return render(request, 'add_connection.html', {'form': form})
    return render(request, 'add_connection.html', {'form': ConnectionForm()})