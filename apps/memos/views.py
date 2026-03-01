from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Memo

@login_required
def memos(request):
    user_memos = Memo.objects.filter(user=request.user)
    context = {
        'academic_memos': user_memos.filter(category='academic'),
        'household_memos': user_memos.filter(category='household'),
        'career_memos': user_memos.filter(category='career'),
    }
    return render(request, 'memos.html', context)

@login_required
def add_memo(request):
    if request.method == 'POST':
        Memo.objects.create(
            user=request.user,
            category=request.POST.get('category'),
            text=request.POST.get('text'),
        )
        return redirect('memos:memos')
    return render(request, 'add_memo.html', {})

@login_required
def delete_memo(request, memo_id):
    Memo.objects.filter(id=memo_id, user=request.user).delete()
    return redirect('memos:memos')