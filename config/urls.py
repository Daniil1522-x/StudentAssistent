from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Главная страница (домашний дашборд, не путать с apps.calendar_app —
    # тот отвечает за пользовательский календарь на /calendar/)
    path('', include('apps.dashboard.urls')),


    path('accounts/', include('apps.accounts.urls')),
    path('disciplines/', include('apps.disciplines.urls')),
    path('connections/', include('apps.connections.urls')),
    path('calendar/', include('apps.calendar_app.urls')),
    path('memos/', include('apps.memos.urls')),
    path('security/', include('apps.security.urls')),
    path('university-info/', include('apps.university.urls')),
    path('sources/', include('apps.sources.urls')),
    path('chat/', include('apps.chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# В DEBUG=False (prod) Django намеренно НЕ отдаёт MEDIA_URL сам — это
# небезопасно/неэффективно и всегда было так по дизайну Django.
# STATIC_URL в проде отдаёт WhiteNoise (настроен в base.py, работает
# независимо от DEBUG). А вот для MEDIA_URL в проде отдельного обработчика
# сейчас нет вообще — сейчас это не проблема, т.к. функций загрузки файлов
# (avatar и т.п.) ещё не реализовано (см. apps/accounts/models.py: поле
# UserProfile.avatar объявлено, но нигде не используется). Как только
# появится реальная загрузка файлов — здесь потребуется nginx location
# для /media/ (или S3/аналог), иначе загруженные файлы будут недоступны.