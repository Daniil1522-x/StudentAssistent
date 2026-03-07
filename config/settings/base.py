from pathlib import Path
from decouple import config

# ────────────────────────────────────────────────
# Пути (BASE_DIR — корень проекта event-site/)
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ────────────────────────────────────────────────
# Основные настройки (переопределяются в dev.py / prod.py)
# ────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []

# ────────────────────────────────────────────────
# Приложения
# ────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_htmx',

    'apps.accounts',
    'apps.disciplines',
    'apps.connections',
    'apps.sources',
    'apps.calendar_app',
    'apps.memos',
    'apps.university',
    'apps.security',
    'apps.common',
    'apps.chat',
    'apps.events',
]

# Django Channels
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


AUTH_USER_MODEL = 'accounts.User'
# ────────────────────────────────────────────────
# Middleware (общие для всех сред)
# ────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# ────────────────────────────────────────────────
# База данных (по умолчанию SQLite — удобно для старта)
# ────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ────────────────────────────────────────────────
# Статические файлы (CSS, JS, изображения)
# ────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ────────────────────────────────────────────────
# Медиа (загруженные файлы: аватарки, фото событий)
# ────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ────────────────────────────────────────────────
# Шаблоны
# ────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

# ────────────────────────────────────────────────
# Дополнительно (WSGI, URLconf, etc.)
# ────────────────────────────────────────────────
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ────────────────────────────────────────────────
# Логин / редиректы (стандартные)
# ────────────────────────────────────────────────
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

# ────────────────────────────────────────────────
# Безопасность (в проде усиливай!)
# ────────────────────────────────────────────────
SECURE_SSL_REDIRECT = False            # в проде True
SESSION_COOKIE_SECURE = False          # в проде True
CSRF_COOKIE_SECURE = False             # в проде True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True