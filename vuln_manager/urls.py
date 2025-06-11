from django.urls import path
from .views import (
    ClienteListView,
    ClienteDetailView,
    ActivoListView,
    ActivoDetailView,
    VulnerabilidadListView,
    VulnerabilidadDetailView,
)

app_name = 'vuln_manager'

urlpatterns = [
    # URLs para Clientes
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),
    
    # URLs para Activos
    path('activos/', ActivoListView.as_view(), name='activo_list'),
    path('activos/<int:pk>/', ActivoDetailView.as_view(), name='activo_detail'),
    
    # URLs para Vulnerabilidades
    path('vulnerabilidades/', VulnerabilidadListView.as_view(), name='vulnerabilidad_list'),
    path('vulnerabilidades/<int:pk>/', VulnerabilidadDetailView.as_view(), name='vulnerabilidad_detail'),
] 