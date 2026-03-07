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

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

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

# ────────────────────────────────────────────────
# Email — всё в консоль, чтобы не спамить реальные ящики
# ────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


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

# media-файлы (аватарки, фото)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ────────────────────────────────────────────────
# Переменные для удобства (можно использовать в шаблонах)
# ────────────────────────────────────────────────
DEVELOPMENT_MODE = True