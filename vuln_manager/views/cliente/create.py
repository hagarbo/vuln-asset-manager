from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from vuln_manager.forms import ClienteCreationForm
from vuln_manager.services.cliente.cliente_service import ClienteService
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository

class ClienteCreateView(RoleRequiredMixin, View):
    template_name = 'vuln_manager/cliente/create.html'
    allowed_roles = ['admin']

    def get(self, request, *args, **kwargs):
        form = ClienteCreationForm(analistas_queryset=UsuarioRepository().get_analistas())
        context = {
            'form': form,
            'form_title': 'Crear Cliente',
            'form_subtitle': 'Crea un nuevo cliente en el sistema',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ClienteCreationForm(request.POST, request.FILES, analistas_queryset=UsuarioRepository().get_analistas())
        if form.is_valid():
            try:
                datos_usuario = {
                    'username': form.cleaned_data['username'],
                    'email': form.cleaned_data['email'],
                    'password': form.cleaned_data['password'],
                }
                datos_cliente = {
                    'nombre': form.cleaned_data['nombre']
                }
                archivo_activos = form.cleaned_data.get('archivo_activos')
                analistas_ids = list(form.cleaned_data['analistas'].values_list('id', flat=True))
                ClienteService().crear_cliente_con_usuario_activos_y_analistas(
                    datos_usuario=datos_usuario,
                    datos_cliente=datos_cliente,
                    archivo_activos=archivo_activos,
                    analistas_ids=analistas_ids
                )
                messages.success(request, 'Cliente creado correctamente.')
                return redirect(reverse_lazy('vuln_manager:cliente_list'))
            except Exception as e:
                messages.error(request, f'Error al crear el cliente: {str(e)}')
        return render(request, self.template_name, {'form': form, 'form_title': 'Crear Cliente', 'form_subtitle': 'Crea un nuevo cliente en el sistema'})