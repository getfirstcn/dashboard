# import urllib3
# import json
# kubehttp=urllib3.PoolManager(
#     num_pools=4,
#     maxsize=4,
#     ca_certs='D:\\src\\devops\\dashboard\\static\\dashboard\\pki\\ca.crt',
#     cert_reqs='CERT_REQUIRED',
#     cert_file='D:\\src\\devops\\dashboard\\static\\dashboard\pki\\front-proxy-client.crt',
#     key_file='D:\\src\\devops\\dashboard\\static\\dashboard\\pki\\front-proxy-client.key'
# )
# data=kubehttp.request('GET', 'https://192.168.137.50:6443/apis/apps/v1/namespaces/kube-system/controllerrevisions')
# print(data.data)
from kubernetes import client, config
from django.shortcuts import loader, render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View, ListView
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from . import repitl
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, User
from django.utils.decorators import method_decorator
import json


perm_add_server = Permission.objects.get(codename='add_server')
@login_required(redirect_field_name='next', login_url='/login/')
@permission_required('dashboard.add_server', login_url='/login/')
def pod_list(request):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    latest_question_list = v1.list_pod_for_all_namespaces(watch=False)
    # print(latest_question_list.__dict__)
    template = loader.get_template('dashboard/pod.html')
    return HttpResponse(template.render({'latest_question_list': latest_question_list}, request))


class ns_list(TemplateView):
    template_name = 'dashboard/namespace.html'

    #@method_decorator(permission_required('dashboard.add_server',  login_url='/login/'))
    def get_context_data(self, **kwargs):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        ns = []
        for i in v1.list_namespace(watch=False).items:
            ns.append(i.metadata.self_link.split('/')[-1])

        context = super(ns_list, self).get_context_data(**kwargs)
        context['ns'] = ns
        return context

    def post(self, request):
        ret = {'status': 0}
        name = request.POST.get('name', None)

        if name:
            try:
                config.load_kube_config()
                v1 = client.CoreV1Api()
                ns = client.V1Namespace()
                ns.metadata = client.V1ObjectMeta(name=name)

                v1.create_namespace(body=ns)

            except Exception as e:
                ret['status'] = 1
                ret['msg'] = e.args

        return JsonResponse(ret, safe=True)

class deploy_list(TemplateView):
    template_name = 'dashboard/deploy.html'

    def get_context_data(self, **kwargs):
        config.load_kube_config()
        v1 = client.AppsV1beta2Api()
        context = super(deploy_list, self).get_context_data(**kwargs)
        deploys = v1.list_deployment_for_all_namespaces().items
        context['deploys'] = deploys
        return context

class service_list(TemplateView):
    template_name = 'dashboard/service.html'
    def get_context_data(self, **kwargs):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        context = super(service_list, self).get_context_data(**kwargs)
        services = v1.list_service_for_all_namespaces(watch=False).items
        context['services'] = services
        return context



class SelectType(View):

    def get(self, request, types):
        print(types)
        if types == 'add':
            return render(request, 'dashboard/dpp.html', {'title': 'rebbot 运维'})
        if types == 'img':
            a = repitl.get_image_name()
            return JsonResponse(a, safe=False)
        if types == 'pj':
            return JsonResponse(repitl.get_project())

        if types == 'ns':
            config.load_kube_config()
            v1 = client.CoreV1Api()
            ns_list = []
            for i in v1.list_namespace(watch=False).items:
                ns_list.append(i.metadata.self_link.split('/'[-1]))
            return JsonResponse(ns_list, safe=False)

        def post(self, request, types):
            if types == 'img':
                pj_id = request.POST.get('pid')
                a = repitl.get_image_name(project_id=pj_id)

                if a:
                    return JsonResponse(a, safe=False)
                else:
                    return JsonResponse('N', safe=False)

                if types == 'tags':
                    repo_name = request.POST.get('image')
                    tags = repitl.get_tags(repo_name)
                    return JsonResponse(tags, safe=False)



