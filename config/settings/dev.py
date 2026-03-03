# config/settings/dev.py
from .base import *  # ← импортируем ВСЁ из base.py (самое важное!)

# Отключение отладочной панели
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: request.user.is_authenticated,
}
# =============================================================================
# РЕЖИМ РАЗРАБОТКИ (dev.py) — всё ниже переопределяет base.py
# =============================================================================

# ────────────────────────────────────────────────
# Основные флаги разработки
# ────────────────────────────────────────────────
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']  # '*' только для тестов, не оставляй в проде!

# ────────────────────────────────────────────────
# Debug Toolbar — только в DEBUG-режиме
# ────────────────────────────────────────────────
INSTALLED_APPS += [
    # 'debug_toolbar',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# ────────────────────────────────────────────────
# Кэширование — dummy в разработке (быстро и без Redis)
# ────────────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Если хочешь подключить Redis позже — раскомментируй:
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

# ────────────────────────────────────────────────
# Email — всё в консоль, чтобы не спамить реальные ящики
# ────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ────────────────────────────────────────────────
# Дополнительные настройки для удобства разработки
# ────────────────────────────────────────────────
# Автоматический релоад шаблонов при изменении
# TEMPLATES[0]['APP_DIRS'] = False  # отключаем автоматическое подключение app_dirs
# TEMPLATES[0]['OPTIONS']['loaders'] = [
#     ('django.template.loaders.cached.Loader', [
#         'django.template.loaders.filesystem.Loader',
#         'django.template.loaders.app_directories.Loader',
#     ]),
# ]

# Показывать подробные ошибки в консоли
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Если используешь media-файлы (аватарки, фото)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ────────────────────────────────────────────────
# Переменные для удобства (можно использовать в шаблонах)
# ────────────────────────────────────────────────
DEVELOPMENT_MODE = True