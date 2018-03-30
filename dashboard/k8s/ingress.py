from django.views.generic.base import TemplateView

class ingress_list(TemplateView):
    template_name = "dashboard/kubernetes/ingresses.html"