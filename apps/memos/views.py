from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import MemoForm
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
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = request.user
            memo.save()
            return redirect('memos:memos')
        return render(request, 'add_memo.html', {'form': form})
    return render(request, 'add_memo.html', {'form': MemoForm()})

@login_required
def delete_memo(request, memo_id):
    Memo.objects.filter(id=memo_id, user=request.user).delete()
    return redirect('memos:memos')