from .activo import (
    ActivoListView,
    ActivoDetailView,
    ActivoCreateView,
    ActivoUpdateView,
    ActivoDeleteView,
)
from .vulnerabilidad import (
    VulnerabilidadListView,
    VulnerabilidadDetailView,
    VulnerabilidadCreateView,
    VulnerabilidadUpdateView,
    VulnerabilidadDeleteView,
)
from .cliente import (
    ClienteListView,
    ClienteDetailView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
)
from .activo_vulnerabilidad import (
    ActivoVulnerabilidadListView,
    ActivoVulnerabilidadDetailView,
    ActivoVulnerabilidadCreateView,
    ActivoVulnerabilidadUpdateView,
    ActivoVulnerabilidadDeleteView,
)
from .auth import (
    CustomLoginView,
    CustomLogoutView,
    UsuarioCreateView,
    UsuarioUpdateView,
)
from .tarea import (
    TareaListView,
    TareaCreateView,
    TareaDetailView,
    TareaUpdateView,
    TareaDeleteView,
)

__all__ = [
    'ClienteListView',
    'ClienteDetailView',
    'ClienteCreateView',
    'ClienteUpdateView',
    'ClienteDeleteView',
    'ActivoListView',
    'ActivoDetailView',
    'ActivoCreateView',
    'ActivoUpdateView',
    'ActivoDeleteView',
    'VulnerabilidadListView',
    'VulnerabilidadDetailView',
    'VulnerabilidadCreateView',
    'VulnerabilidadUpdateView',
    'VulnerabilidadDeleteView',
    'ActivoVulnerabilidadListView',
    'ActivoVulnerabilidadDetailView',
    'ActivoVulnerabilidadCreateView',
    'ActivoVulnerabilidadUpdateView',
    'ActivoVulnerabilidadDeleteView',
    'CustomLoginView',
    'CustomLogoutView',
    'UsuarioCreateView',
    'UsuarioUpdateView',
    'TareaListView',
    'TareaCreateView',
    'TareaDetailView',
    'TareaUpdateView',
    'TareaDeleteView',
] 