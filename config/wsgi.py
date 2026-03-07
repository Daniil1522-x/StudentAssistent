import os

from django.core.wsgi import get_wsgi_application

# Укажи правильный модуль настроек (dev для разработки)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()