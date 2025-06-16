from django.views.generic import UpdateView
from django.urls import reverse_lazy
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoVulnerabilidadUpdateView(RoleRequiredMixin, UpdateView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/form.html'
    success_url = reverse_lazy('vuln_manager:activo_vulnerabilidad_list')
    allowed_roles = ['admin', 'analista']
    fields = '__all__'

    def get_queryset(self):
        repository = ActivoVulnerabilidadRepository()
        user = self.request.user

        if user.rol == 'admin':
            return repository.get_all()
        elif user.rol == 'analista':
            return repository.get_by_activos_analista(user.id)
        return repository.model.objects.none()

    def form_valid(self, form):
        repository = ActivoVulnerabilidadRepository()
        instance = repository.update(self.object.id, **form.cleaned_data)
        if instance:
            return super().form_valid(form)
        return self.form_invalid(form) 