from django.views.generic import TemplateView, View, ListView
from dashboard.models import Server
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required

class GroupList(ListView):

    template_name = 'dashboard/server/server.html'
    model = Server
    paginate_by = 10

class Addserver(View):
    @login_required(redirect_field_name='next', login_url='/login/')
    @permission_required('dashboard.add_server', login_url='/login/')
    def post(self, request):
        hostname = request.POST.get('hostname')
        ip = request.POST.get('address')
        status = request.POST.get('status')
        print(hostname, ip, status)
        try:
            Server.obects.create(hostname=hostname, ip=ip, status=str(status))
        except Exception as e:
            print(e)
        return HttpResponseRedirect('/server/list/')

    @login_required(redirect_field_name='next', login_url='/login/')
    @permission_required('dashboard.delete_server', login_url='/login/')
    def delete(self, request):
        pass

    @login_required(redirect_field_name='next', login_url='/login/')
    @permission_required('dashboard.change_server', login_url='/login/')
    def update(self, request):
        pass
    2

    2