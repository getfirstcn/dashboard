from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse, JsonResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect

class IndexView(View):
    #method_decorator 装饰器将函数装饰器转换成方法装饰器，这样它才可以用于实例方法上
    @method_decorator(login_required)
    def get(self,request):
        return render(request, 'dashboard/public/index.html')


class LogIn(View):
    def get(self, request):
        return render(request, 'dashboard/login.html', {'title': 'rebbot 运维'})

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username)
        ret = {'status': 0}
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                ret['nexturl'] = '/dashboard/'
            else:
                ret['status'] = 2
                ret['errmsg'] = 'err'
                ret['username'] = username
                print(ret)
            return JsonResponse(ret, safe=True)
class DefaultView(View):
    def get(self, request):
        return HttpResponse('default')

class LogOut(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponse('账户退出成功')

def permit(request):
    return render(request, 'public/permit.html')



# Create your views here.
