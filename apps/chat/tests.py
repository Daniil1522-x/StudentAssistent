from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase

from apps.chat.consumers import ChatConsumer
from apps.chat.models import ChatRoom, Message

User = get_user_model()


def make_communicator(room_name, user):
    """
    Собирает WebsocketCommunicator напрямую на ChatConsumer, минуя
    AuthMiddlewareStack (её механизм сессий/кук не нужен для юнит-теста) —
    scope['user'] и url_route выставляются вручную, как это в реальности
    делает AuthMiddlewareStack + URLRouter.
    """
    communicator = WebsocketCommunicator(
        ChatConsumer.as_asgi(), f'/ws/chat/{room_name}/'
    )
    communicator.scope['user'] = user
    communicator.scope['url_route'] = {'kwargs': {'room_name': room_name}}
    return communicator


class ChatConsumerAuthTests(TransactionTestCase):
    """
    TASK 02 acceptance: анонимное WS-подключение закрывается сразу,
    без accept() и без истории сообщений.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='den', password='pass12345')
        self.other_user = User.objects.create_user(username='alice', password='pass12345')
        self.room = ChatRoom.objects.create(name='testroom', created_by=self.other_user)
        Message.objects.create(room=self.room, user=self.other_user, content='secret history line')

    async def test_anonymous_connection_is_rejected(self):
        communicator = make_communicator('testroom', AnonymousUser())
        connected, _ = await communicator.connect()
        self.assertFalse(connected)
        await communicator.disconnect()

    async def test_anonymous_user_never_receives_history(self):
        """
        До фикса анонимное соединение принималось (accept()) и получало
        последние 50 сообщений комнаты ДО какой-либо проверки авторизации.
        """
        communicator = make_communicator('testroom', AnonymousUser())
        connected, _ = await communicator.connect()
        self.assertFalse(connected)
        # После отказа в connect() сообщений быть не должно вовсе.
        self.assertTrue(await communicator.receive_nothing(timeout=0.2))
        await communicator.disconnect()

    async def test_authenticated_user_connects_and_receives_history(self):
        communicator = make_communicator('testroom', self.user)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'secret history line')
        self.assertEqual(response['username'], 'alice')

        await communicator.disconnect()

    async def test_disconnect_before_auth_pass_does_not_raise(self):
        """
        disconnect() не должен падать с AttributeError, если соединение
        было закрыто в connect() до того, как room_group_name был установлен.
        """
        communicator = make_communicator('testroom', AnonymousUser())
        await communicator.connect()
        # Не должно бросить исключение.
        await communicator.disconnect()
