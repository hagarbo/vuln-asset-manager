from django.views.generic import TemplateView
from vuln_manager.mixins.permissions import AdminRequiredMixin
from vuln_manager.repository.tarea.tarea_repository import TareaRepository
from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'vuln_manager/dashboard/admin/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Repositorios
        tarea_repo = TareaRepository()
        usuario_repo = UsuarioRepository()
        vulnerabilidad_repo = VulnerabilidadRepository()

        # Datos para el dashboard
        context['tareas_pendientes'] = tarea_repo.count_programadas()
        context['total_usuarios'] = usuario_repo.count()
        context['total_vulnerabilidades'] = vulnerabilidad_repo.count()
        context['ultimas_tareas'] = tarea_repo.get_latest(5)

        return context 