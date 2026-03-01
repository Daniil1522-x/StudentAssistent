from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Discipline

@login_required
def disciplines(request):
    user_disciplines = Discipline.objects.filter(user=request.user)
    context = {
        'disciplines': {d.name: d for d in user_disciplines}
    }
    return render(request, 'disciplines.html', context)

@login_required
def add_discipline(request):
    if request.method == 'POST':
        Discipline.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            teacher=request.POST.get('teacher'),
            course=int(request.POST.get('course')),
            hours=int(request.POST.get('hours')),
            performance=request.POST.get('performance', ''),
            grade=request.POST.get('grade') or None,
            notes=request.POST.get('notes', ''),
        )
        return redirect('disciplines:disciplines')
    return render(request, 'add_discipline.html', {})