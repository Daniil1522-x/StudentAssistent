from .prod import *  # noqa: F401,F403

# manage.py test использует django.test.Client, который по умолчанию делает
# обычные HTTP-запросы (wsgi.url_scheme='http'), а не HTTPS. С
# SECURE_SSL_REDIRECT=True (как в prod.py) любой такой запрос получает
# 301-редирект на https://, что ломает почти все view-тесты — это
# несовместимость тестового клиента с этой настройкой, а не баг приложения.
# Реальные пользователи в проде всегда идут через HTTPS за reverse proxy
# (см. SECURE_PROXY_SSL_HEADER в prod.py) — эта настройка их не касается.
# Используется ТОЛЬКО для прогона manage.py test в CI против настоящего
# PostgreSQL/Redis; сам prod.py (и `check --deploy` в CI) остаётся
# непереопределённым и проверяется отдельно.
SECURE_SSL_REDIRECT = False
