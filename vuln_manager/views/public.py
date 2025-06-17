from django.views.generic import TemplateView

class PublicHomeView(TemplateView):
    template_name = "home.html"