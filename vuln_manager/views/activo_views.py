from django.views.generic import ListView, DetailView
from vuln_manager.models import Activo

class ActivoListView(ListView):
    model = Activo
    template_name = 'vuln_manager/activo_list.html'
    context_object_name = 'activos'
    ordering = ['-created_at']

class ActivoDetailView(DetailView):
    model = Activo
    template_name = 'vuln_manager/activo_detail.html'
    context_object_name = 'object' 