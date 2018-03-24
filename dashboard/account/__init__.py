from django.contrib.auth import login,authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect

def account_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect('/deployments/')

    else:
        return HttpResponse('<p>无效的登陆，没有用户名</p>')

def account_logout(request):
    logout(request)
    return HttpResponse("<p>退出成功</>")
