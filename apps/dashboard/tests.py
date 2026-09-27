from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class DashboardRenameSmokeTest(TestCase):
    def test_home_page_renders_under_new_namespace(self):
        User.objects.create_user(username='smoketest', password='pass12345')
        self.client.login(username='smoketest', password='pass12345')

        self.assertEqual(reverse('dashboard:home'), '/')
        self.assertEqual(reverse('dashboard:index'), '/')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('session_periods', response.context['calendar'])

    def test_navbar_and_sidebar_links_resolve(self):
        """base.html ссылается на dashboard:home и dashboard:index — если бы
        рефакторинг переименования забыл какую-то из этих ссылок, рендер
        любой страницы, использующей base.html, упал бы с NoReverseMatch."""
        User.objects.create_user(username='smoketest2', password='pass12345')
        self.client.login(username='smoketest2', password='pass12345')
        response = self.client.get(reverse('disciplines:disciplines'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_after_registration_uses_new_namespace(self):
        response = self.client.post(reverse('accounts:register'), data={
            'username': 'newuser', 'password1': 'SomeStrongPass123!', 'password2': 'SomeStrongPass123!',
        })
        self.assertRedirects(response, '/')
