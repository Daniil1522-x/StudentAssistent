# apps/accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('events:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html') # accounts/...

def logout_view(request):
    logout(request)
    return redirect('index')  # или 'login'

@login_required
def personal_info(request):
    """
    Отображает страницу редактирования личной информации
    """
    profile = request.user.profile  # предполагается, что есть модель Profile (OneToOneField с User)

    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'personal_info.html', context)


@login_required
def update_personal_info(request):
    """
    Сохраняет изменения личной информации (AJAX или обычный POST)
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Метод не POST'}, status=405)

    profile = request.user.profile

    request.user.email = request.POST.get('email', request.user.email)
    request.user.save()

    try:
        profile.name = request.POST.get('name', profile.name)
        profile.course = int(request.POST.get('course', profile.course))
        profile.group_number = request.POST.get('group_number', profile.group_number)
        profile.faculty = request.POST.get('faculty', profile.faculty)
        profile.education_form = request.POST.get('education_form', profile.education_form)
        profile.phone = request.POST.get('phone', profile.phone or '')
        profile.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            messages.success(request, 'Данные успешно обновлены!')
            return redirect('accounts:personal_info')

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        messages.error(request, f'Ошибка: {str(e)}')
        return redirect('accounts:personal_info')