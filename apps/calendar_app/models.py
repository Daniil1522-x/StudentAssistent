from django.db import models
from django.conf import settings

class Event(models.Model):
    EVENT_TYPES = [
        ('important', 'Важная дата'),
        ('session', 'Сессия'),
        ('holiday', 'Каникулы'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=200)
    date = models.DateField('Дата')
    description = models.TextField('Описание', blank=True)
    event_type = models.CharField('Тип', max_length=20, choices=EVENT_TYPES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.date})"

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['date']