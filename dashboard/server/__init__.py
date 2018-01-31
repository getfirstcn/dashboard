from django.views.generic import TemplateView, View, ListView
from dashboard.models import Server
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

class GroupList(ListView):

    template_name = 'dashboard/server/server.html'
    model = Server
    paginate_by = 10

class Addserver(View):
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

    def delete(self, request):
        pass

    def update(self, request):
        pass
    2

    2