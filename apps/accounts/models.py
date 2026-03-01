# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Расширенная модель пользователя"""
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')

    # Переопределяем related_name, чтобы избежать конфликта с auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # уникальное имя
        blank=True,
        verbose_name='группы',
        help_text='Группы, к которым принадлежит пользователь.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # уникальное имя
        blank=True,
        verbose_name='права пользователя',
        help_text='Конкретные права пользователя.',
    )

    def __str__(self):
        return self.get_full_name() or self.get_username()  # ← используем метод, IDE не ругается

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProfile(models.Model):
    """Личная информация пользователя"""
    EDUCATION_FORMS = [
        ('очная', 'Очная'),
        ('заочная', 'Заочная'),
        ('очно-заочная', 'Очно-заочная'),
        ('вечерняя', 'Вечерняя'),
    ]

    user: User = models.OneToOneField(  # ← type hint для IDE
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    name = models.CharField('ФИО', max_length=100, blank=True)
    course = models.PositiveIntegerField(
        'Курс',
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        null=True,
        blank=True
    )
    education_form = models.CharField(
        'Форма обучения',
        max_length=20,
        choices=EDUCATION_FORMS,
        blank=True
    )
    group_number = models.CharField('Номер группы', max_length=20, blank=True)
    faculty = models.CharField('Факультет', max_length=100, blank=True)
    speciality = models.CharField('Специальность', max_length=200, blank=True)
    phone = models.CharField('Дополнительный телефон', max_length=20, blank=True)
    address = models.TextField('Адрес', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Исправляем, чтобы IDE не ругался
        return f"{self.name or self.user.get_username()} ({self.group_number or 'нет группы'})"

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['name', 'group_number']
        indexes = [
            models.Index(fields=['group_number', 'course']),
        ]