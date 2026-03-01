from django.db import models
from django.conf import settings

class Memo(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Учебные'),
        ('household', 'Бытовые'),
        ('career', 'Карьерные'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}: {self.text[:50]}"