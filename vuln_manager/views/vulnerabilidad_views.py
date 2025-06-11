from django.views.generic import ListView, DetailView
from vuln_manager.models import Vulnerabilidad

class VulnerabilidadListView(ListView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad_list.html'
    context_object_name = 'vulnerabilidades'
    ordering = ['-fecha_modificacion']

class VulnerabilidadDetailView(DetailView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad_details.html'
    context_object_name = 'vulnerabilidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 