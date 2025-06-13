from django.urls import path
from .views import (
    ClienteListView,
    ClienteDetailView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
    ActivoListView,
    ActivoDetailView,
    ActivoCreateView,
    ActivoUpdateView,
    ActivoDeleteView,
    VulnerabilidadListView,
    VulnerabilidadDetailView,
    VulnerabilidadCreateView,
    VulnerabilidadUpdateView,
    VulnerabilidadDeleteView,
    ActivoVulnerabilidadListView,
    ActivoVulnerabilidadDetailView,
    ActivoVulnerabilidadCreateView,
    ActivoVulnerabilidadUpdateView,
    ActivoVulnerabilidadDeleteView,
    CustomLoginView,
    CustomLogoutView,
    UsuarioCreateView,
    UsuarioUpdateView,
)

app_name = 'vuln_manager'

urlpatterns = [
    # URLs para Clientes
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/crear/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # URLs para Activos
    path('activos/', ActivoListView.as_view(), name='activo_list'),
    path('activos/<int:pk>/', ActivoDetailView.as_view(), name='activo_detail'),
    path('activos/create/', ActivoCreateView.as_view(), name='activo_create'),
    path('activos/<int:pk>/update/', ActivoUpdateView.as_view(), name='activo_update'),
    path('activos/<int:pk>/delete/', ActivoDeleteView.as_view(), name='activo_delete'),
    
    # URLs para Vulnerabilidades
    path('vulnerabilidades/', VulnerabilidadListView.as_view(), name='vulnerabilidad_list'),
    path('vulnerabilidades/<int:pk>/', VulnerabilidadDetailView.as_view(), name='vulnerabilidad_detail'),
    path('vulnerabilidades/create/', VulnerabilidadCreateView.as_view(), name='vulnerabilidad_create'),
    path('vulnerabilidades/<int:pk>/update/', VulnerabilidadUpdateView.as_view(), name='vulnerabilidad_update'),
    path('vulnerabilidades/<int:pk>/delete/', VulnerabilidadDeleteView.as_view(), name='vulnerabilidad_delete'),

    # URLs para Activo-Vulnerabilidad
    path('activo-vulnerabilidad/', ActivoVulnerabilidadListView.as_view(), name='activo_vulnerabilidad_list'),
    path('activo-vulnerabilidad/<int:pk>/', ActivoVulnerabilidadDetailView.as_view(), name='activo_vulnerabilidad_detail'),
    path('activo-vulnerabilidad/create/', ActivoVulnerabilidadCreateView.as_view(), name='activo_vulnerabilidad_create'),
    path('activo-vulnerabilidad/<int:pk>/update/', ActivoVulnerabilidadUpdateView.as_view(), name='activo_vulnerabilidad_update'),
    path('activo-vulnerabilidad/<int:pk>/delete/', ActivoVulnerabilidadDeleteView.as_view(), name='activo_vulnerabilidad_delete'),

    # URLs para Autenticación y Gestión de Usuarios
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
] 