from django.views.generic.base import TemplateView

class serviceacount_list(TemplateView):
    template_name = "dashboard/kubernetes/serviceaccounts.html"