from django.views.generic import TemplateView, View, ListView
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

class LW(View):
    #template_name = 'user/wuser.html'
    #model = User
   # paginate_by = 10

    @method_decorator(login_required)
    @method_decorator(permission_required('auth.view_user_list'))
    def get(self, request):
        return HttpResponse("have permission")



