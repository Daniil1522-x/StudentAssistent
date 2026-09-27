from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.connections.models import Connection

User = get_user_model()


class AddConnectionFormTests(TestCase):
    """
    ModelForm вместо сырого request.POST.get(): раньше при пустом
    category/text форма молча редиректила ничего не сохранив, без
    единого сообщения об ошибке.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='den4', password='pass12345')
        self.client = Client()
        self.client.login(username='den4', password='pass12345')

    def test_valid_submission_creates_connection(self):
        response = self.client.post(reverse('connections:add_connection'), data={
            'category': 'Семья', 'text': 'Мама помогает с расписанием',
        })
        self.assertRedirects(response, reverse('connections:connections'))
        self.assertTrue(Connection.objects.filter(user=self.user, category='Семья').exists())

    def test_empty_text_shows_error_instead_of_silent_fail(self):
        response = self.client.post(reverse('connections:add_connection'), data={
            'category': 'Семья', 'text': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Connection.objects.filter(user=self.user).exists())
        self.assertIn('text', response.context['form'].errors)

    def test_empty_category_shows_error_instead_of_silent_fail(self):
        response = self.client.post(reverse('connections:add_connection'), data={
            'category': '', 'text': 'Что-то важное',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Connection.objects.filter(user=self.user).exists())
        self.assertIn('category', response.context['form'].errors)
