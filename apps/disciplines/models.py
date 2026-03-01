# apps/disciplines/models.py (или где лежит Discipline)
from django.db import models
from django.conf import settings   # ← добавляем этот импорт
from django.core.validators import MinValueValidator, MaxValueValidator


class Discipline(models.Model):
    PERFORMANCE_CHOICES = [
        ('отлично', 'Отлично'),
        ('хорошо', 'Хорошо'),
        ('удовлетворительно', 'Удовлетворительно'),
        ('неудовлетворительно', 'Неудовлетворительно'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,               # ← вот это главное изменение
        on_delete=models.CASCADE,
        related_name='disciplines'
    )
    name = models.CharField('Название дисциплины', max_length=200)
    teacher = models.CharField('Преподаватель', max_length=200)
    course = models.PositiveIntegerField('Курс', validators=[MinValueValidator(1), MaxValueValidator(6)])
    hours = models.PositiveIntegerField('Часы')
    performance = models.CharField('Успеваемость', max_length=20, choices=PERFORMANCE_CHOICES, blank=True)
    grade = models.PositiveIntegerField('Оценка', validators=[MinValueValidator(2), MaxValueValidator(5)], null=True, blank=True)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['course', 'name']