import base64
import hashlib

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models


def get_fernet():
    """Текущий (актуальный) Fernet-инстанс — на отдельном FERNET_KEY."""
    return Fernet(settings.FERNET_KEY.encode())


def get_legacy_fernet():
    """
    Старый способ вывода ключа: SHA256(SECRET_KEY).
    Используется только один раз — командой rotate_fernet_key —
    чтобы расшифровать данные, записанные до перехода на FERNET_KEY.
    Не использовать в обычном коде.
    """
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


class EncryptedField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return get_fernet().decrypt(value.encode()).decode()
        except Exception:
            return value

    def get_prep_value(self, value):
        if value is None:
            return value
        return get_fernet().encrypt(value.encode()).decode()


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = EncryptedField()
    url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service} — {self.login}"

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['service']