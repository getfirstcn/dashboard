from django.views.generic.base import TemplateView

class role_list(TemplateView):
    template_name = "dashboard/kubernetes/roles.html"