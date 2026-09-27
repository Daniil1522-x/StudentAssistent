from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.memos.models import Memo

User = get_user_model()


class AddMemoFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='den5', password='pass12345')
        self.client = Client()
        self.client.login(username='den5', password='pass12345')

    def test_valid_submission_creates_memo(self):
        response = self.client.post(reverse('memos:add_memo'), data={
            'category': 'academic', 'text': 'Сдать курсовую до пятницы',
        })
        self.assertRedirects(response, reverse('memos:memos'))
        self.assertTrue(Memo.objects.filter(user=self.user, category='academic').exists())

    def test_invalid_category_rejected(self):
        """
        choices=CATEGORY_CHOICES на модели раньше никак не проверялся при
        Memo.objects.create() — значение вне списка тихо записывалось в БД.
        Через ModelForm невалидная категория должна отклоняться.
        """
        response = self.client.post(reverse('memos:add_memo'), data={
            'category': 'not-a-real-category', 'text': 'Текст',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Memo.objects.filter(user=self.user).exists())
        self.assertIn('category', response.context['form'].errors)

    def test_empty_text_rejected(self):
        response = self.client.post(reverse('memos:add_memo'), data={
            'category': 'academic', 'text': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Memo.objects.filter(user=self.user).exists())


class DeleteMemoOwnershipTests(TestCase):
    """
    delete_memo уже фильтровал по user=request.user до этого рефакторинга —
    здесь просто закрываем отсутствовавшее тестовое покрытие (regression-тест).
    """

    def setUp(self):
        self.owner = User.objects.create_user(username='owner3', password='pass12345')
        self.other = User.objects.create_user(username='other3', password='pass12345')
        self.memo = Memo.objects.create(user=self.owner, category='academic', text='secret note')

    def test_user_cannot_delete_other_users_memo(self):
        client = Client()
        client.login(username='other3', password='pass12345')
        client.post(reverse('memos:delete_memo', args=[self.memo.id]))
        self.assertTrue(Memo.objects.filter(pk=self.memo.id).exists())

    def test_owner_can_delete_own_memo(self):
        client = Client()
        client.login(username='owner3', password='pass12345')
        client.post(reverse('memos:delete_memo', args=[self.memo.id]))
        self.assertFalse(Memo.objects.filter(pk=self.memo.id).exists())
