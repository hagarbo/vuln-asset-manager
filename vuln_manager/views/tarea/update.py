from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.core.serializers.json import DjangoJSONEncoder
import json
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.tipo_tarea import TipoTarea
from vuln_manager.forms.tarea.tarea_form import TareaForm

class TareaUpdateView(RoleRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'vuln_manager/tarea/form.html'
    success_url = reverse_lazy('vuln_manager:tarea_list')
    allowed_roles = ['admin']

    def get_queryset(self):
        return super().get_queryset().select_related('tipo', 'creada_por')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipos_tarea = TipoTarea.objects.filter(activo=True)
        context['tipos_tarea_json'] = json.dumps(
            list(tipos_tarea.values('id', 'nombre', 'codigo', 'parametros', 'descripcion')),
            cls=DjangoJSONEncoder
        )
        return context 