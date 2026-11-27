from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('imoveis.urls')),
    path('contas/login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('contas/', include('django.contrib.auth.urls')),
    path('usuarios/', include('usuarios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
