"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from vuln_manager.mixins.auth import CustomLoginRequiredMixin
from vuln_manager.views.public import PublicHomeView
from vuln_manager.views.dashboard.redirect import HomeView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PublicHomeView.as_view(), name='home'),  # Landing pública
    path('dashboard/', HomeView.as_view(), name='dashboard_redirect'),  # Redirección por rol
    path('', include('vuln_manager.urls')),
]

if settings.DEBUG:
    # Servir archivos estáticos desde STATICFILES_DIRS en desarrollo
    for static_dir in settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=static_dir)
