"""
Módulo de repositorios para Vuln-Asset-Manager.
Cada repositorio maneja las operaciones de base de datos para su entidad correspondiente.
"""

from .vulnerabilidad import VulnerabilidadRepository
from .activo import ActivoRepository
from .cliente import ClienteRepository
from .alerta import AlertaRepository
from .tarea import TareaRepository
from .usuario import UsuarioRepository

__all__ = [
    'VulnerabilidadRepository',
    'ActivoRepository',
    'ClienteRepository',
    'AlertaRepository',
    'TareaRepository',
    'UsuarioRepository',
] 