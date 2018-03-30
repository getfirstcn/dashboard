from django.views.generic.base import TemplateView

class endpoint_list(TemplateView):
    template_name = "dashboard/kubernetes/endpoints.html"