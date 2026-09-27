from cryptography.fernet import Fernet
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from django.test import Client, TestCase
from django.urls import reverse

from apps.security.models import Account, get_fernet, get_legacy_fernet

User = get_user_model()


def _raw_password(account_id):
    """Читает столбец password напрямую из БД, в обход EncryptedField.from_db_value."""
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT password FROM security_account WHERE id = %s', [account_id]
        )
        return cursor.fetchone()[0]


class DuplicateServiceNameTests(TestCase):
    """
    TASK 05 acceptance: два Account с одинаковым service оба видны в UI —
    раньше dict-по-service в passwords() молча "терял" один из них.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='den2', password='pass12345')

    def test_duplicate_service_names_both_displayed(self):
        Account.objects.create(user=self.user, service='github', login='den-work')
        Account.objects.create(user=self.user, service='github', login='den-personal')

        client = Client()
        client.login(username='den2', password='pass12345')
        response = client.get(reverse('security:passwords'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['passwords']['accounts']), 2)
        self.assertContains(response, 'den-work')
        self.assertContains(response, 'den-personal')


class DeleteAccountOwnershipTests(TestCase):
    """TASK 08 acceptance: нельзя удалить чужой Account."""

    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')
        self.account = Account.objects.create(
            user=self.owner, service='github', login='owner-login', password='secret',
        )

    def test_owner_can_delete_own_account(self):
        client = Client()
        client.login(username='owner', password='pass12345')

        response = client.post(
            reverse('security:delete_account', args=[self.account.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Account.objects.filter(pk=self.account.id).exists())

    def test_user_cannot_delete_other_users_account(self):
        client = Client()
        client.login(username='other', password='pass12345')

        client.post(
            reverse('security:delete_account', args=[self.account.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        # Запись должна остаться нетронутой — filter(user=...).delete() на
        # чужом id просто не находит строк, а не падает с ошибкой.
        self.assertTrue(Account.objects.filter(pk=self.account.id).exists())

    def test_delete_account_requires_post(self):
        client = Client()
        client.login(username='owner', password='pass12345')

        response = client.get(reverse('security:delete_account', args=[self.account.id]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Account.objects.filter(pk=self.account.id).exists())

    def test_delete_account_requires_login(self):
        client = Client()
        response = client.post(reverse('security:delete_account', args=[self.account.id]))
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Account.objects.filter(pk=self.account.id).exists())


class RevealPasswordOwnershipTests(TestCase):
    """TASK 08 acceptance: нельзя получить чужой пароль по id."""

    def setUp(self):
        self.owner = User.objects.create_user(username='owner2', password='pass12345')
        self.other = User.objects.create_user(username='other2', password='pass12345')
        self.account = Account.objects.create(
            user=self.owner, service='gitlab', login='owner-login', password='my-real-password',
        )

    def test_owner_can_reveal_own_password(self):
        client = Client()
        client.login(username='owner2', password='pass12345')

        response = client.post(
            reverse('security:reveal_password', args=[self.account.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['password'], 'my-real-password')

    def test_user_cannot_reveal_other_users_password(self):
        client = Client()
        client.login(username='other2', password='pass12345')

        response = client.post(
            reverse('security:reveal_password', args=[self.account.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        # 404, а не 403 — не подтверждаем даже факт существования записи.
        self.assertEqual(response.status_code, 404)

    def test_reveal_password_requires_post(self):
        client = Client()
        client.login(username='owner2', password='pass12345')

        response = client.get(reverse('security:reveal_password', args=[self.account.id]))

        self.assertEqual(response.status_code, 405)

    def test_reveal_password_requires_login(self):
        client = Client()
        response = client.post(reverse('security:reveal_password', args=[self.account.id]))
        self.assertNotEqual(response.status_code, 200)


class AddAccountAjaxTests(TestCase):
    """TASK 09 acceptance: submit формы в модалке получает JSON, а не redirect-HTML."""

    def setUp(self):
        self.user = User.objects.create_user(username='ajax-user', password='pass12345')

    def test_add_account_ajax_returns_json(self):
        client = Client()
        client.login(username='ajax-user', password='pass12345')

        response = client.post(
            reverse('security:add_account'),
            data={'service': 'slack', 'login': 'den', 'password': 'x', 'url': '', 'notes': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertTrue(Account.objects.filter(user=self.user, service='slack').exists())

    def test_add_account_without_ajax_header_still_redirects(self):
        """Обычная (не-AJAX) отправка формы — прежнее поведение, редирект."""
        client = Client()
        client.login(username='ajax-user', password='pass12345')

        response = client.post(
            reverse('security:add_account'),
            data={'service': 'notion', 'login': 'den', 'password': 'x', 'url': '', 'notes': ''},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Account.objects.filter(user=self.user, service='notion').exists())


class AddAccountFormValidationTests(TestCase):
    """
    ModelForm вместо сырого request.POST.get() для add_account: невалидный
    ввод не должен создавать запись ни на полностраничной, ни на AJAX-ветке.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='ajax-user2', password='pass12345')
        self.client = Client()
        self.client.login(username='ajax-user2', password='pass12345')

    def test_missing_required_field_full_page(self):
        response = self.client.post(reverse('security:add_account'), data={
            'service': '', 'login': 'den', 'password': 'x', 'url': '', 'notes': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Account.objects.filter(user=self.user).exists())
        self.assertIn('service', response.context['form'].errors)

    def test_missing_required_field_ajax_returns_json_error(self):
        """
        Модалка на passwords.html ждёт {success: False, error: "..."},
        а не полный HTML формы с ошибками — это отдельная ветка ответа.
        """
        response = self.client.post(
            reverse('security:add_account'),
            data={'service': '', 'login': 'den', 'password': 'x', 'url': '', 'notes': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('error', data)
        self.assertFalse(Account.objects.filter(user=self.user).exists())

    def test_invalid_url_rejected(self):
        response = self.client.post(reverse('security:add_account'), data={
            'service': 'test', 'login': 'den', 'password': 'x', 'url': 'not-a-url', 'notes': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Account.objects.filter(user=self.user).exists())
        self.assertIn('url', response.context['form'].errors)


class FernetKeySeparationTests(TestCase):
    """
    TASK 01 acceptance: FERNET_KEY больше не выводится из SECRET_KEY,
    и существующие пароли переживают миграцию на новый ключ.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='den', password='pass12345')

    def test_new_account_uses_dedicated_fernet_key(self):
        """Новая запись шифруется/читается через settings.FERNET_KEY, а не SECRET_KEY."""
        account = Account.objects.create(
            user=self.user,
            service='github',
            login='den',
            password='super-secret-1',
        )
        account.refresh_from_db()
        self.assertEqual(account.password, 'super-secret-1')

        raw_value = _raw_password(account.id)
        self.assertEqual(get_fernet().decrypt(raw_value.encode()).decode(), 'super-secret-1')

    def test_get_fernet_ignores_secret_key(self):
        """get_fernet() зависит только от FERNET_KEY, смена SECRET_KEY на него не влияет."""
        fernet_key = Fernet.generate_key().decode()

        with self.settings(SECRET_KEY='secret-key-value-A', FERNET_KEY=fernet_key):
            token = get_fernet().encrypt(b'value')

        with self.settings(SECRET_KEY='secret-key-value-B', FERNET_KEY=fernet_key):
            # Тот же FERNET_KEY при другом SECRET_KEY должен расшифровать то же значение.
            self.assertEqual(get_fernet().decrypt(token).decode(), 'value')

    def test_legacy_fernet_depends_on_secret_key(self):
        """get_legacy_fernet(), в отличие от get_fernet(), завязан на SECRET_KEY — это и есть баг, который фиксит TASK 01."""
        with self.settings(SECRET_KEY='secret-key-value-A'):
            token = get_legacy_fernet().encrypt(b'value')

        with self.settings(SECRET_KEY='secret-key-value-B'):
            with self.assertRaises(Exception):
                get_legacy_fernet().decrypt(token)

    def test_account_password_survives_key_migration(self):
        """
        Запись, зашифрованная старым (SECRET_KEY-производным) ключом,
        после rotate_fernet_key читается корректно новым FERNET_KEY.
        """
        legacy_encrypted = get_legacy_fernet().encrypt(b'legacy-password-value').decode()

        account = Account.objects.create(
            user=self.user, service='old-service', login='den', password='placeholder',
        )
        # Подменяем в БД напрямую на "исторически" зашифрованное старым ключом
        # значение, минуя EncryptedField.get_prep_value (который бы зашифровал
        # новым ключом при обычном save()).
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE security_account SET password = %s WHERE id = %s',
                [legacy_encrypted, account.id],
            )

        call_command('rotate_fernet_key')

        account.refresh_from_db()
        self.assertEqual(account.password, 'legacy-password-value')

    def test_rotate_fernet_key_dry_run_does_not_change_data(self):
        legacy_encrypted = get_legacy_fernet().encrypt(b'legacy-password-value').decode()

        account = Account.objects.create(
            user=self.user, service='old-service-2', login='den', password='placeholder',
        )
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE security_account SET password = %s WHERE id = %s',
                [legacy_encrypted, account.id],
            )

        call_command('rotate_fernet_key', '--dry-run')

        self.assertEqual(_raw_password(account.id), legacy_encrypted)
