from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from vuln_manager.models import Usuario
from vuln_manager.mixins.permissions import AdminRequiredMixin
from vuln_manager.forms.usuario import UsuarioCreationForm, UsuarioChangeForm

class UsuarioListView(AdminRequiredMixin, ListView):
    """
    Vista para listar usuarios.
    Solo accesible por administradores.
    """
    model = Usuario
    template_name = 'vuln_manager/usuario/list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    ordering = ['username']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar por búsqueda si se proporciona
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(username__icontains=search)
        
        # Filtrar por rol
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(rol=role)
        
        return queryset

class UsuarioCreateView(AdminRequiredMixin, CreateView):
    """
    Vista para crear usuarios.
    Solo accesible por administradores.
    """
    form_class = UsuarioCreationForm
    template_name = 'registration/usuario_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Usuario {form.instance.username} creado exitosamente.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar el perfil de usuario.
    """
    form_class = UsuarioChangeForm
    template_name = 'registration/usuario_form.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form) 