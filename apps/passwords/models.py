from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings


class PasswordVault(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_vault'
    )
    salt = models.BinaryField(max_length=16)
    encrypted_key = models.BinaryField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Хранилище паролей'
        verbose_name_plural = 'Хранилища паролей'


class EncryptedPassword(models.Model):
    vault = models.ForeignKey(PasswordVault, on_delete=models.CASCADE, related_name='passwords')
    service_name = models.CharField('Название сервиса', max_length=200)
    encrypted_login = models.TextField('Зашифрованный логин')
    encrypted_password = models.TextField('Зашифрованный пароль')
    url = models.URLField('URL', blank=True)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = 'Зашифрованный пароль'
        verbose_name_plural = 'Зашифрованные пароли'
        ordering = ['service_name']


class PasswordRecommendation(models.Model):
    text = models.TextField('Рекомендация')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Рекомендация по паролям'
        verbose_name_plural = 'Рекомендации по паролям'
        ordering = ['order']