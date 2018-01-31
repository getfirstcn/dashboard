from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.models import Group, User, Permission, ContentType
from django.http import JsonResponse, HttpResponse, QueryDict, HttpResponseBadRequest
from django.core import serializers
import logging


logger = logging.getLogger('opsweb')

class GroupListView(ListView):
    model = Group
    template_name = 'dashboard/user/grouplist.html'

    def post(self, request):
        ret = {'status': 0}
        name = request.POST.get('name', None)
        print(name)
        if name:
            try:
                group = Group()
                group.name = name
                group.save()
            except Exception as e:
                ret['msg'] = e.args
                ret['status'] = 2
        return JsonResponse(ret, safe=True)

class GroupView(View):
    def get(self, request):
        uid = request.GET.get('uid')
        print(uid)
        user = User.objects.get(pk=uid)
        groups = [i for i in Group.objects.all() if i not in user.groups.all()]
        groups = Group.objects.all()
        return HttpResponse(serializers.serialize('json', groups), content_type='application/json')

class UserGroup(View):
    def post(self, request):
        ret = {'status': 0}
        gid = request.POST.get('gid')
        uid = request.POST.get('uid')
        try:
            user = User.objects.get(pk=uid)
        except Exception as e:
            logger.error(e)
            ret['status'] = 1
            ret['msg'] = e
            return JsonResponse(ret, safe=True)
        try:
            group = Group.objects.get(pk=gid)
        except Exception as e:
            logger.error(e)
            ret['status'] = 1
            ret['msg'] = e
            return JsonResponse(ret, safe=True)
    def get(self, request):
        gid = request.GET.get('gid', None)
        try:
            groups = Group.objects.get(pk=gid)
            groups = [{'id': i.id, 'name': i.username, 'email': i.email} for i in groups.user_set.all()]
            print(groups)
            return JsonResponse(groups, safe=False)
        except:
            return JsonResponse([], safe=False)

    def delete(self, request):
        ret = {'status': 0}
        res_obj = QueryDict(request.body)
        uid = res_obj.get('uid')
        gid = res_obj.get('gid')
        print(uid,gid)
        try:
            user = User.objects.get(pk=uid)
            group = Group.objects.get(pk=gid)
            group.user_set.remove(user)
        except Exception as e:
            ret['status'] = 1
            ret['msg'] = e.args
        return JsonResponse(ret)

class PermissionList(TemplateView):
    template_name = 'user/group_permission_list.html'

    def get_context_data(self, **kwargs):
        context = super(PermissionList, self).get_context_data(**kwargs)
        context['group'] = self.request.GET.get('gid')
        context['content_type'] = ContentType.objects.all()
        context['msg'] = 'err'
        context['group_permissions'] = self.get_group_permissions()
        return context
    def get_group_permissions(self):
        gid = self.request.GET.get('gid')
        group = Group.objects.get(pk=gid)
        return [per.id for per in group.permissions.all()]
    def post(self, request):
        gid = request.POST.get('group')
        pms_id = request.POST.getlist('permission')
        print(pms_id)
        g = Group.objects.get('group')
        if pms_id:
            pms_obj = Permission.objects.filter(id__in=pms_id)
            g.permissions = pms_obj
        return HttpResponseBadRequest('/group/list/')

    def delete(self, request):
        pass

    def update(self, request):
        pass