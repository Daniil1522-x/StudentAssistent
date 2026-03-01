# apps/accounts/apps.py
from django.apps import AppConfig  # ← добавляем импорт


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'

    def ready(self):
        # Импорт сигналов должен быть здесь, чтобы избежать циклических импортов
        import apps.accounts.signals  # noqa: F401 — подавляем предупреждение Unused import