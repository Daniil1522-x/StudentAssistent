from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import DisciplineForm
from .models import Discipline


@login_required
def disciplines(request):
    user_disciplines = Discipline.objects.filter(user=request.user)
    context = {
        'disciplines': user_disciplines,
    }
    return render(request, 'disciplines.html', context)

@login_required
def add_discipline(request):
    if request.method == 'POST':
        form = DisciplineForm(request.POST)
        if form.is_valid():
            discipline = form.save(commit=False)
            discipline.user = request.user
            discipline.save()
            return redirect('disciplines:disciplines')
        return render(request, 'add_discipline.html', {'form': form})
    return render(request, 'add_discipline.html', {'form': DisciplineForm()})