from pathlib import Path
from decouple import config

# ────────────────────────────────────────────────
# Пути (BASE_DIR — корень проекта event-site/)
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ────────────────────────────────────────────────
# Основные настройки (переопределяются в dev.py / prod.py)
# ────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY') # ← поменяй в prod!

DEBUG = config('DEBUG', default=False, cast=bool)  # ← обязательно False в base! В dev.py ставим True

ALLOWED_HOSTS = []  # ← в dev.py ставим ['*'] или конкретные хосты

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


    # Сторонние пакеты (добавляй по мере необходимости)
    # 'debug_toolbar',           # только в dev
    'django_htmx',             # если используешь HTMX

    # Твои приложения (все в apps/)
    'apps.accounts',
    'apps.disciplines',
    'apps.connections',
    'apps.sources',
    'apps.calendar_app',
    'apps.memos',
    'apps.university',
    'apps.security',           # пароли + безопасность
    'apps.common',             # общие утилиты, контекст-процессоры
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

# Кастомная модель пользователя (если используешь)
AUTH_USER_MODEL = 'accounts.User'  # ← раскомментируй, если создал свою модель User

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
    'django_htmx.middleware.HtmxMiddleware',  # для HTMX
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
STATICFILES_DIRS = [BASE_DIR / 'static']           # исходники (src/)
STATIC_ROOT = BASE_DIR / 'staticfiles'             # для collectstatic в проде

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
        'DIRS': [BASE_DIR / 'templates'],              # глобальные шаблоны
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Если добавишь свой процессор (например для темы)
                # 'apps.common.context_processors.theme_settings',
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
LOGIN_REDIRECT_URL = '/'               # после логина — на главную
LOGOUT_REDIRECT_URL = '/accounts/login/'  # после выхода — на логин
LOGIN_URL = '/accounts/login/'         # куда редиректит @login_required

# ────────────────────────────────────────────────
# Безопасность (в проде усиливай!)
# ────────────────────────────────────────────────
SECURE_SSL_REDIRECT = False            # в проде True
SESSION_COOKIE_SECURE = False          # в проде True
CSRF_COOKIE_SECURE = False             # в проде True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True