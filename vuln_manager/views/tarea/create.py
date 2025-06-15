from django.shortcuts import render, redirect
from django.views.generic import View
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.forms import TareaForm

class TareaCreateView(RoleRequiredMixin, View):
    template_name = 'vuln_manager/tarea/create.html'
    allowed_roles = ['admin']

    def get(self, request):
        form = TareaForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.creado_por = request.user
            tarea.save()
            return redirect('vuln_manager:tarea_list')
        return render(request, self.template_name, {'form': form})