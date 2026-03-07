from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Account

@login_required
def passwords(request):
    user_accounts = Account.objects.filter(user=request.user)
    accounts_dict = {a.service: a for a in user_accounts}
    context = {
        'passwords': {
            'accounts': accounts_dict,
        },
        'recommendations': [
            'Используйте уникальные пароли для каждого сервиса',
            'Пароль должен содержать минимум 12 символов',
            'Используйте буквы, цифры и спецсимволы',
        ]
    }
    return render(request, 'passwords.html', context)

@login_required
def add_account(request):
    if request.method == 'POST':
        Account.objects.create(
            user=request.user,
            service=request.POST.get('service'),
            login=request.POST.get('login'),
            password=request.POST.get('password'),
            url=request.POST.get('url') or None,
            notes=request.POST.get('notes', ''),
        )
        return redirect('security:passwords')
    return render(request, 'add_account.html', {})

@login_required
def security(request):
    return render(request, 'security.html')