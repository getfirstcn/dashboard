from django.views.generic import TemplateView, View, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from dashboard.models import Department, Profile
from django.conf import settings

class LW(ListView):
    template_name = 'dashboard/user/userlist.html'
    model = User
    paginate_by = 10


    @login_required(redirect_field_name='next', login_url='/login/')
    #@permission_required('auth.view_user_list', login_url='/login/')
    def get(self, request, *args, **kwargs):
        return super(LW, self).get(request, *args, **kwargs)

class Modify_status(View):
    @login_required(redirect_field_name='next', login_url='/login/')
    @permission_required('auth.change_user', login_url='/login/')
    def post(self, request):
        ret = {'status': 0}
        user_id = request.POST.get('user_id', None)
        print(user_id)
        try:
            user = User.objects.get(pk=user_id)
            print(user)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
        except User.DoesNotExist:
            ret['status'] = 1
            print(ret)
            ret['errmsg'] = 'User is not exist'
            print(ret['errmsg'])
            return JsonResponse(ret, safe=True)


class ModifyDepartmentView(TemplateView):
     template_name = 'dashboard/user/department.html'

     def get_context_data(self, **kwargs):
         context = super(ModifyDepartmentView, self).get_context_data(**kwargs)
         context['departments'] = Department.object.all()
         context['user_obj'] = get_object_or_404(User, id=self.request.GET.get('user', None))
         return context
     #@method_decorator(login_required)
     #@method_decorator(permission_required('dashboard.change_department', login_url=settings.TEMPLATE_403))
     def get(self, request, *args, **kwargs):
         self.request = request
         return super(ModifyDepartmentView, self).get(self, *args, **kwargs)

     @login_required(redirect_field_name='next', login_url='/login/')
     @permission_required('auth.change_group', login_url='/login/')
     def post(self, request):
         user_id = request.POST.get('user', None)
         dpart_id = request.POST.get('department', None)
         if not user_id or not dpart_id:
             raise Http404
         try:
             user_obj = User.objects.get(pk=user_id)
             depart_obj = request.POST.get('department', None)
         except:
             raise Http404
         else:
             try:
                 user_id.profile.department = depart_obj
                 user_obj.profile.save()
             except:
                 p = Profile(user=user_obj, department=depart_obj)
                 p.user.save()
                 p.department.save()
                 p.save()
                 return redirect('/user/userlist/')
             else:
                 return redirect('/user/userlist')

class ModifyPhoneView(TemplateView):
    template_name = 'dashboard/user/modifyphone.html'
    def get_context_data(self, **kwargs):
        context = super(ModifyPhoneView, self).get_context_data(**kwargs)
        context['user_obj'] = get_object_or_404(User, pk=self.request.GET.get('user', None))
        return context
    def get(self, request, *args, **kwargs):
        self.request = request
        return super(ModifyPhoneView, self).get(self, *args, **kwargs)
    @login_required(redirect_field_name='next', login_url='/login/')
    @permission_required('auth.change_user', login_url='/login/')
    def post(self, request):
        user_id = request.POST.get('user', None)
        phone_num = request.POST.get('pnum', None)
        if not user_id or not phone_num:
            raise Http404
        try:
            user_obj = User.objects.get(pk=user_id)
            user_obj.profile.phone = phone_num
            user_obj.profile.save()
            print(settings.TEMPLATE_JUMP)
            return render(request, settings.TEMPLATE_JUMP, {'status':0, 'etx_url': '/user/userlist/'})
        except:
            return HttpResponse('err')

def getCurrenUser(request):
    username=request.user.username
    print(username)
    return JsonResponse({'username': username})
