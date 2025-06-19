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
    UsuarioListView,
    TareaListView,
    TareaCreateView,
    TareaDetailView,
    TareaUpdateView,
    TareaDeleteView,
    AlertaListView,
    AlertaDetailView,
    AlertaUpdateView,
    ejecutar_tarea
)
from .views.dashboard.admin import AdminDashboardView
from .views.dashboard.analista import AnalistaDashboardView
from .views.cliente.mis_clientes import MisClientesView
from vuln_manager.views.dashboard.cliente import ClienteDashboardView
from vuln_manager.views.activo.list import ActivoListView
from vuln_manager.views.alerta.list import AlertaListView

app_name = 'vuln_manager'

urlpatterns = [
    # URLs de autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # URLs de dashboard
    path('dashboard/admin/', AdminDashboardView.as_view(), name='dashboard_admin'),
    path('dashboard/analista/', AnalistaDashboardView.as_view(), name='dashboard_analista'),
    path('dashboard/cliente/', ClienteDashboardView.as_view(), name='dashboard_cliente'),
    
    # URLs de usuarios
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/create/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/update/', UsuarioUpdateView.as_view(), name='usuario_update'),
    
    # URLs de clientes
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/create/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/update/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/delete/', ClienteDeleteView.as_view(), name='cliente_delete'),
    path('mis-clientes/', MisClientesView.as_view(), name='mis_clientes'),
    
    # URLs de activos
    path('activos/', ActivoListView.as_view(), name='activo_list'),
    path('activos/<int:pk>/', ActivoDetailView.as_view(), name='activo_detail'),
    path('activos/create/', ActivoCreateView.as_view(), name='activo_create'),
    path('activos/<int:pk>/update/', ActivoUpdateView.as_view(), name='activo_update'),
    path('activos/<int:pk>/delete/', ActivoDeleteView.as_view(), name='activo_delete'),
    
    # URLs de vulnerabilidades
    path('vulnerabilidades/', VulnerabilidadListView.as_view(), name='vulnerabilidad_list'),
    path('vulnerabilidades/<int:pk>/', VulnerabilidadDetailView.as_view(), name='vulnerabilidad_detail'),
    path('vulnerabilidades/<int:pk>/editar/', VulnerabilidadUpdateView.as_view(), name='vulnerabilidad_update'),
    path('vulnerabilidades/<int:pk>/eliminar/', VulnerabilidadDeleteView.as_view(), name='vulnerabilidad_delete'),
    
    # URLs de activo-vulnerabilidad
    path('activo-vulnerabilidad/', ActivoVulnerabilidadListView.as_view(), name='activo_vulnerabilidad_list'),
    path('activo-vulnerabilidad/<int:pk>/', ActivoVulnerabilidadDetailView.as_view(), name='activo_vulnerabilidad_detail'),
    path('activo-vulnerabilidad/create/', ActivoVulnerabilidadCreateView.as_view(), name='activo_vulnerabilidad_create'),
    path('activo-vulnerabilidad/<int:pk>/update/', ActivoVulnerabilidadUpdateView.as_view(), name='activo_vulnerabilidad_update'),
    path('activo-vulnerabilidad/<int:pk>/delete/', ActivoVulnerabilidadDeleteView.as_view(), name='activo_vulnerabilidad_delete'),
    
    # URLs de tareas
    path('tareas/', TareaListView.as_view(), name='tarea_list'),
    path('tareas/create/', TareaCreateView.as_view(), name='tarea_create'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail'),
    path('tareas/<int:pk>/update/', TareaUpdateView.as_view(), name='tarea_update'),
    path('tareas/<int:pk>/delete/', TareaDeleteView.as_view(), name='tarea_delete'),
    path('tareas/<int:pk>/ejecutar/', ejecutar_tarea, name='ejecutar_tarea'),
    
    # URLs de alertas
    path('alertas/', AlertaListView.as_view(), name='alerta_list'),
    path('alertas/<int:pk>/', AlertaDetailView.as_view(), name='alerta_detail'),
    path('alertas/<int:pk>/editar/', AlertaUpdateView.as_view(), name='alerta_update'),
    path('cliente/activos/', ActivoListView.as_view(), name='cliente_activo_list'),
    path('cliente/alertas/', AlertaListView.as_view(), name='cliente_alerta_list'),
] 