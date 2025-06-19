from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django import forms
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.alerta.alerta_repository import AlertaRepository

class AlertaUpdateView(RoleRequiredMixin, UpdateView):
    model = Alerta
    template_name = 'vuln_manager/alerta/update.html'
    context_object_name = 'alerta'
    allowed_roles = ['admin', 'analista']
    fields = ['estado', 'analista_asignado', 'notas']
    success_url = reverse_lazy('vuln_manager:alerta_list')

    def get_queryset(self):
        user = self.request.user
        repository = AlertaRepository()
        if user.es_admin:
            return repository.get_all().select_related('vulnerabilidad', 'activo', 'activo__cliente')
        elif user.es_analista:
            return repository.get_by_analista(user)
        return repository.get_none()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        # Si es analista, limitar las opciones
        if user.es_analista:
            # Solo puede asignarse a sí mismo
            form.fields['analista_asignado'].queryset = user.__class__.objects.filter(id=user.id)
            form.fields['analista_asignado'].initial = user
            
            # Solo puede cambiar a estados permitidos
            if self.object.estado == 'nueva':
                form.fields['estado'].choices = [
                    choice for choice in Alerta.ESTADO_CHOICES 
                    if choice[0] in ['en_proceso', 'ignorada']
                ]
            elif self.object.estado == 'en_proceso':
                form.fields['estado'].choices = [
                    choice for choice in Alerta.ESTADO_CHOICES 
                    if choice[0] in ['resuelta', 'ignorada']
                ]
        
        return form

    def form_valid(self, form):
        estado = form.cleaned_data['estado']
        analista = form.cleaned_data['analista_asignado']
        notas = (form.cleaned_data.get('notas') or '').strip()

        # Validaciones de negocio
        if estado == 'en_proceso' and not analista:
            form.add_error('analista_asignado', 'Debes asignar un analista para poner la alerta en proceso.')
            return self.form_invalid(form)

        if estado in ['resuelta', 'ignorada']:
            if not analista:
                form.add_error('analista_asignado', 'Debes asignar un analista para resolver o ignorar la alerta.')
                return self.form_invalid(form)
            if not notas:
                form.add_error('notas', 'Debes escribir una nota para resolver o ignorar la alerta.')
                return self.form_invalid(form)

        # Actualizar fecha de resolución si se marca como resuelta o ignorada
        if estado in ['resuelta', 'ignorada']:
            form.instance.fecha_resolucion = timezone.now()
            form.instance.resuelta_por = self.request.user
        # Actualizar fecha de actualización
        form.instance.fecha_actualizacion = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, 
            f'Alerta {self.object.vulnerabilidad.cve_id} actualizada correctamente.'
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Editar Alerta',
            'breadcrumbs': [
                {'label': 'Dashboard', 'url': '/dashboard/'},
                {'label': 'Alertas', 'url': '/alertas/'},
                {'label': f'Alerta {self.object.vulnerabilidad.cve_id}', 'url': reverse_lazy('vuln_manager:alerta_detail', kwargs={'pk': self.object.pk})},
                {'label': 'Editar', 'url': None}
            ],
        })
        return context 