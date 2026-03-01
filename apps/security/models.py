from django.db import models
from django.conf import settings

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service} — {self.login}"