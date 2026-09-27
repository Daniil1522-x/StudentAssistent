from decouple import Csv, config

from .base import *  # noqa: F401,F403

# ────────────────────────────────────────────────
# Базовые флаги
# ────────────────────────────────────────────────
DEBUG = False

# Реальный(е) домен(ы) через запятую в .env, например:
#   ALLOWED_HOSTS=example.com,www.example.com
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Откуда разрешён CSRF-POST (нужен Django 4+ при HTTPS): полный origin со схемой.
#   CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv())

# ────────────────────────────────────────────────
# База данных — PostgreSQL (в dev/base — SQLite)
# Требует пакет psycopg (добавлен в pyproject.toml).
# ────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# ────────────────────────────────────────────────
# HTTPS / cookies / HSTS
# Приложение должно стоять за reverse proxy (nginx), который терминирует TLS
# и прокидывает X-Forwarded-Proto — иначе Django не узнает, что запрос был
# по HTTPS, и уйдёт в бесконечный redirect-loop.
# ────────────────────────────────────────────────
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# HSTS_PRELOAD сознательно не включаю: preload-список браузеров — операция
# «в один конец», её стоит включать отдельным осознанным шагом, а не по умолчанию.
SECURE_HSTS_PRELOAD = False

X_FRAME_OPTIONS = 'DENY'

# ────────────────────────────────────────────────
# Логирование — в консоль (systemd/docker сам соберёт stdout в журнал)
# ────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

DEVELOPMENT_MODE = False

# ────────────────────────────────────────────────
# Channel layer — Redis вместо InMemoryChannelLayer из base.py.
# InMemoryChannelLayer работает только внутри одного процесса: при
# daphne/uvicorn с несколькими worker'ами или несколькими контейнерами
# broadcast сообщений чата не доходит до клиентов на других процессах.
# Требует пакет channels-redis (добавлен в pyproject.toml) и отдельно
# запущенный Redis.
#   REDIS_URL=redis://localhost:6379          — без пароля
#   REDIS_URL=redis://:password@localhost:6379 — с паролем
#   REDIS_URL=rediss://localhost:6379          — TLS
# ────────────────────────────────────────────────
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [config('REDIS_URL', default='redis://localhost:6379')],
        },
    }
}
