"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

"""
WSGI config for config project.
"""

import os

from django.core.wsgi import get_wsgi_application

# Укажи правильный модуль настроек (dev для разработки)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()