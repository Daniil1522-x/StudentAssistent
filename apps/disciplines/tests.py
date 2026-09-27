from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.disciplines.models import Discipline

User = get_user_model()


class DisciplineDuplicateNameTests(TestCase):
    """
    TASK 05 acceptance: две Discipline с одинаковым name обе видны в UI —
    раньше dict-по-name в disciplines() молча "терял" одну из них.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='den', password='pass12345')
        self.client = Client()
        self.client.login(username='den', password='pass12345')

    def test_duplicate_discipline_names_both_displayed(self):
        Discipline.objects.create(
            user=self.user, name='Матанализ', teacher='Иванов', course=1, hours=100,
        )
        Discipline.objects.create(
            user=self.user, name='Матанализ', teacher='Петров', course=2, hours=80,
        )

        response = self.client.get(reverse('disciplines:disciplines'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['disciplines']), 2)
        # Оба преподавателя должны быть в отрендеренной странице.
        self.assertContains(response, 'Иванов')
        self.assertContains(response, 'Петров')


class AddDisciplineFormTests(TestCase):
    """
    Проверка перехода add_discipline с сырого request.POST.get()/int() на
    DisciplineForm: невалидный ввод должен возвращать форму с ошибками
    (200), а не падать 500-й ошибкой ValueError.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='den3', password='pass12345')
        self.client = Client()
        self.client.login(username='den3', password='pass12345')

    def test_valid_submission_creates_discipline(self):
        response = self.client.post(reverse('disciplines:add_discipline'), data={
            'name': 'Физика', 'teacher': 'Сидоров', 'course': '2', 'hours': '60',
            'performance': 'хорошо', 'grade': '', 'notes': '',
        })
        self.assertRedirects(response, reverse('disciplines:disciplines'))
        self.assertTrue(Discipline.objects.filter(user=self.user, name='Физика').exists())

    def test_non_numeric_course_does_not_crash(self):
        """
        До фикса int(request.POST.get('course')) с нечисловым значением
        падал с ValueError -> 500. Теперь форма должна вернуть 200 с ошибкой
        валидации и ничего не сохранять.
        """
        response = self.client.post(reverse('disciplines:add_discipline'), data={
            'name': 'Химия', 'teacher': 'Кузнецов', 'course': 'не число', 'hours': '60',
            'performance': 'хорошо', 'grade': '', 'notes': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Discipline.objects.filter(user=self.user, name='Химия').exists())
        self.assertTrue(response.context['form'].errors)

    def test_course_out_of_range_rejected(self):
        """MinValueValidator/MaxValueValidator модели должны сработать через форму."""
        response = self.client.post(reverse('disciplines:add_discipline'), data={
            'name': 'История', 'teacher': 'Орлов', 'course': '99', 'hours': '60',
            'performance': 'хорошо', 'grade': '', 'notes': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Discipline.objects.filter(user=self.user, name='История').exists())
        self.assertIn('course', response.context['form'].errors)

    def test_missing_required_field_rejected(self):
        response = self.client.post(reverse('disciplines:add_discipline'), data={
            'name': '', 'teacher': 'Орлов', 'course': '1', 'hours': '60',
            'performance': 'хорошо', 'grade': '', 'notes': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.context['form'].errors)
