# apps/common/models.py
from django.db import models
from django.conf import settings   # ← добавляем этот импорт

class ConnectionCategory(models.Model):
    name = models.CharField('Название категории', max_length=100)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория связей'
        verbose_name_plural = 'Категории связей'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Connection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,               # ← вот это главное изменение
        on_delete=models.CASCADE,
        related_name='connections'
    )
    category = models.ForeignKey(ConnectionCategory, on_delete=models.CASCADE, related_name='connections')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    contact_info = models.TextField('Контактная информация', blank=True)
    is_important = models.BooleanField('Важное', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'