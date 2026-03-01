# apps/accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создаёт профиль при создании пользователя.
    """
    if created:
        # Импорт внутри функции — защита от циклических импортов
        from .models import UserProfile
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет изменения профиля при обновлении пользователя.
    """
    try:
        instance.profile.save()
    except AttributeError:
        # Если профиля почему-то нет — создаём
        from .models import UserProfile
        UserProfile.objects.create(user=instance)