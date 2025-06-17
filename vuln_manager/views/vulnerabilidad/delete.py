from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository

class VulnerabilidadDeleteView(RoleRequiredMixin, DeleteView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:vulnerabilidad_list')
    allowed_roles = ['admin']

    def delete(self, request, *args, **kwargs):
        try:
            vuln = self.get_object()
            nombre = str(vuln)
            repository = VulnerabilidadRepository()
            if repository.delete(vuln.id):
                messages.success(request, f'Vulnerabilidad "{nombre}" eliminada correctamente.')
                return super().delete(request, *args, **kwargs)
            else:
                messages.error(request, 'No se pudo eliminar la vulnerabilidad.')
                return self.get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Error al eliminar la vulnerabilidad: {str(e)}')
            return self.get(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Eliminar {self.model._meta.verbose_name.title()}"
        context['page_subtitle'] = f"¿Estás seguro de que deseas eliminar {self.object}?"
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Vulnerabilidades", "url": "/vulnerabilidades/"},
            {"label": "Eliminar"}
        ]
        return context