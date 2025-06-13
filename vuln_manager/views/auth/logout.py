from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    """
    Vista personalizada para el logout.
    """
    next_page = reverse_lazy('home') 