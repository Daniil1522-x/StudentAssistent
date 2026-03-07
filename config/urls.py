from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Главная страница
    path('', include('apps.events.urls')),


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