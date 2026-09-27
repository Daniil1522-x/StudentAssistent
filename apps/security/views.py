from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AccountForm
from .models import Account


@login_required
def passwords(request):
    user_accounts = Account.objects.filter(user=request.user)
    context = {
        'passwords': {
            'accounts': user_accounts,
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
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            if is_ajax:
                return JsonResponse({'success': True})
            return redirect('security:passwords')

        if is_ajax:
            # Модалка на passwords.html ждёт {success, error} — не полный
            # HTML с формой, как полностраничная версия ниже.
            first_error = next(iter(form.errors.values()))[0]
            return JsonResponse({'success': False, 'error': first_error})
        return render(request, 'add_account.html', {'form': form})

    return render(request, 'add_account.html', {'form': AccountForm()})

@login_required
@require_POST
def delete_account(request, account_id):
    # filter(...).delete() вместо get(...).delete(): если account_id
    # принадлежит другому пользователю, queryset пуст и delete() молча
    # не тронет 0 строк — чужую запись удалить нельзя.
    Account.objects.filter(pk=account_id, user=request.user).delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('security:passwords')

@login_required
@require_POST
def reveal_password(request, account_id):
    # get_object_or_404 с user=request.user: запрос на чужой account_id
    # получает 404, а не 403 — не подтверждает даже сам факт существования
    # чужой записи.
    account = get_object_or_404(Account, pk=account_id, user=request.user)
    return JsonResponse({'password': account.password})

@login_required
def security(request):
    return render(request, 'security.html')