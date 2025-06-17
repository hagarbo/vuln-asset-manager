from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from vuln_manager.models import Cliente, Usuario
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.cliente.cliente_repository import ClienteRepository
from vuln_manager.forms.cliente.update import ClienteUpdateForm

class ClienteUpdateView(RoleRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteUpdateForm
    template_name = 'vuln_manager/cliente/create.html'
    success_url = reverse_lazy('vuln_manager:cliente_list')
    allowed_roles = ['admin']

    def get_queryset(self):
        user = self.request.user
        repository = ClienteRepository()
        if user.es_admin:
            return repository.get_all()
        return repository.get_none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.es_admin:
            context['form'].fields['analistas'].queryset = Usuario.objects.filter(rol='analista')
        
        context['form_title'] = 'Editar Cliente'
        context['form_subtitle'] = 'Modifica los datos del cliente'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Clientes", "url": "/clientes/"},
            {"label": "Editar"}
        ]
        context['card_title'] = 'Datos del Cliente'
            
        return context 

    def form_valid(self, form):
        try:
            repository = ClienteRepository()
            instance = repository.update(self.object.id, **form.cleaned_data)
            if instance:
                messages.success(self.request, f'Cliente "{instance.nombre}" actualizado correctamente.')
                return super().form_valid(form)
            messages.error(self.request, 'No se pudo actualizar el cliente.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar el cliente: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form) 