import json
import re

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        # Проверка авторизации — до accept() и до выдачи истории сообщений.
        # Анонимное соединение закрывается сразу, ничего не получая.
        if not user.is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', self.room_name)
        self.room_group_name = f'chat_{safe_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Отправить историю сообщений
        messages = await self.get_messages()
        for msg in messages:
            await self.send(text_data=json.dumps({
                'message': msg['content'],
                'username': msg['user__username'],
                'timestamp': msg['created_at'].strftime('%H:%M'),
            }))

    async def disconnect(self, close_code):
        # Если соединение было закрыто в connect() до auth-проверки,
        # room_group_name ещё не установлен — group_discard делать не нужно.
        if not hasattr(self, 'room_group_name'):
            return
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']

        # Проверка авторизации
        if not user.is_authenticated:
            await self.close()
            return

        # Валидация сообщения
        message = data.get('message', '').strip()
        if not message:
            return

        await self.save_message(user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def get_messages(self):
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            return list(room.messages.values('content', 'user__username', 'created_at').order_by('-created_at')[:50])[::-1]
        except ChatRoom.DoesNotExist:
            return []

    @database_sync_to_async
    def save_message(self, user, content):
        room, _ = ChatRoom.objects.get_or_create(
            name=self.room_name,
            defaults={'created_by': user}
        )
        Message.objects.create(room=room, user=user, content=content)