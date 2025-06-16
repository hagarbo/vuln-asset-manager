from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
import json
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.forms.tarea.tarea_form import TareaForm
from vuln_manager.models.tarea.tipo_tarea import TipoTarea

class TareaCreateView(RoleRequiredMixin, View):
    template_name = 'vuln_manager/tarea/form.html'
    allowed_roles = ['admin']

    def get(self, request):
        form = TareaForm()
        tipos_tarea = TipoTarea.objects.filter(activo=True)
        tipos_tarea_json = json.dumps(
            [{
                'id': t.id,
                'codigo': t.codigo,
                'nombre': t.nombre,
                'parametros': t.parametros,
                'descripcion': t.descripcion
            } for t in tipos_tarea],
            cls=DjangoJSONEncoder
        )
        return render(request, self.template_name, {
            'form': form,
            'tipos_tarea_json': tipos_tarea_json
        })

    def post(self, request):
        form = TareaForm(request.POST)
        if form.is_valid():
            try:
                tarea = form.save(commit=False)
                tarea.creada_por = request.user
                tarea.save()
                estado = "Programada" if tarea.estado == "programada" else "Pausada"
                messages.success(
                    request,
                    f'Tarea "{tarea.tipo.nombre}" creada exitosamente. Estado: {estado}'
                )
                return redirect('vuln_manager:tarea_list')
            except Exception as e:
                messages.error(request, f'Error al crear la tarea: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        tipos_tarea = TipoTarea.objects.filter(activo=True)
        tipos_tarea_json = json.dumps(
            [{
                'id': t.id,
                'codigo': t.codigo,
                'nombre': t.nombre,
                'parametros': t.parametros,
                'descripcion': t.descripcion
            } for t in tipos_tarea],
            cls=DjangoJSONEncoder
        )
        return render(request, self.template_name, {
            'form': form,
            'tipos_tarea_json': tipos_tarea_json
        })