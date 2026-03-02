from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ChatRoom


@login_required
def chat_list(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            ChatRoom.objects.get_or_create(name=name, defaults={'created_by': request.user})
        return redirect('chat:chat_list')
    rooms = ChatRoom.objects.all().order_by('-created_at')
    return render(request, 'chat/chat_list.html', {'rooms': rooms})


@login_required
def chat_room(request, room_name):
    room, _ = ChatRoom.objects.get_or_create(
        name=room_name,
        defaults={'created_by': request.user}
    )
    return render(request, 'chat/chat_room.html', {'room': room})