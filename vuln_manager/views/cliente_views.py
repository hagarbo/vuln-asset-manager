from django.views.generic import ListView, DetailView
from vuln_manager.models import Cliente

class ClienteListView(ListView):
    model = Cliente
    template_name = 'vuln_manager/cliente_list.html'
    context_object_name = 'clientes'
    ordering = ['-created_at']

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'vuln_manager/cliente_detail.html'
    context_object_name = 'object' 