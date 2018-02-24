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
from . import repitl,dp,image
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, User
from django.utils.decorators import method_decorator
import json
import requests
from pprint import pprint
import time


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

@method_decorator(login_required(redirect_field_name='next', login_url='/login/'), name='dispatch')
@method_decorator(permission_required('dashboard.add_server', login_url='/login/'), name='dispatch')
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
                if types == 'dep':
                    ns = request.POST.get('ns')
                    config.load_kube_config()
                    v1 = client.AppsV1beta2Api
                    ret = []
                    tmp = v1.list_namespaced_deployment(namespace=ns).items
                    for i in tmp:
                        ret.append(i.metadata.name)
                    return JsonResponse(ret, safe=False)
                if types == 'svc':
                    ns = request.POST.get('ns')
                    print(ns)
                    config.load_kube_config()
                    v1 = client.CoreV1Api()
                    ret = []
                    tmp = v1.list_namespaced_service(ns).items
                    for i in tmp:
                        ret.append(i.metadata.name)
                    return JsonResponse(ret, safe=False)

class add_mod_deploy(View):
    def POST(self, request, types):
        ret = {'status': 0}
        if types == 'add':
            try:
                if not request.POST.get('ns', None):
                    ret['status'] = 404
                    ret['msg'] = 'ns不能为空'
                    return JsonResponse(ret, safe=True)
                else:
                    ns = request.POST.get('ns')
                    print(type(ns))
                if not request.POST.get('image', None):
                    ret['status'] = 404
                    ret['msg'] = 'Image不能为空'
                    return JsonResponse(ret, safe=True)
                else:
                    msg = request.POST.get('image')
                if not request.POST.get('tags'):
                    ret['status'] = 404
                    ret['msg'] = 'tags不能为空'
                    return JsonResponse(ret, safe=True)
                else:
                    tags = request.POST.get('tags')
                if not request.POST.get('rc', safe=True):
                    ret['status'] = 1
                    ret['msg'] = 'Image不能为空'
                    return JsonResponse(ret, safe=True)
                else:
                    rc = int(request.POST.get('rc'))
                if not request.POST.get('env', None):
                    ret['status'] = 1
                    ret['msg'] = 'Image不能为空'
                    return JsonResponse(ret, safe=True)
                else:
                    env = request.POST.get('env')
                print(ns, msg, tags, rc, env)
                config.load_kube_config()
                extensions_v1beta1 = client.ExtensionsV1beta1Api()
                deploy = dp.create_deployment_object(tags=tags, images=msg, rc=rc, envs=env)
                ret['status'] = 0
                ret['msg'] = '%s添加成功' % 'goo'
                return JsonResponse(ret, safe=True)
            except Exception as e:
                ret['status'] = 1
                ret['msg'] = e
                return JsonResponse(ret, safe=True)
        if types == 'delete':
            ns = request.POST.get('ns_name').encode('utf-8')
            dp_name = request.POST.get('dp_name').encode('utf-8')
            ret = {'status': 0}
            if dp_name is None:
                ret['status'] = 100
                ret['msg'] = 'ns_name or dp_name is None'
                return JsonResponse(ret)
            else:
                try:
                    config.load_kube_config()
                    extensions_v1beta1 = client.ExtensionsV1beta1Api()
                    dp.delete_deployment(extensions_v1beta1, ns=ns, images=dp_name)
                    ret['status'] = 0
                    ret['msg'] = 'ok'
                except Exception as e:
                    ret['status'] = 55
                    ret['msg'] = e
                return JsonResponse(ret)

class deploy_add(TemplateView):
    template_name = 'dashboard/kubernetes/addDeployment.html'

    def get_context_data(self, **kwargs):
        r = requests.get('http://hub.heshidai.com/api/search')
        projects = r.json()['project']
        repositories = r.json()['repository']
        context = super().get_context_data(**kwargs)
        context['projects'] = projects
        context['repositories'] = repositories
        return context

def repository_select(request):
    project = request.POST.get('project')
    r = requests.get('http://hub.heshidai.com/api/search')
    repositories = r.json()['repository']
    repositoryname=[]
    for i in repositories:
        if project in i['repository_name']:
            repositoryname.append(i['repository_name'])
    return JsonResponse({"repositorires": repositoryname})

def image_tag_get(request):
    imagename=request.POST.get('imagename')
    print(imagename)
    image_url="http://hub.heshidai.com/api/repositories/" + imagename + "/tags?detail=1"
    r=requests.get(image_url)
    tags=[]
    for img in r.json():
        tags.append(img['tag'])
    # print(tags)
    return JsonResponse({"tag":tags})

def deployment_apply(request):
    def createService(servicePort, applyName):
        V1servicePort = client.V1ServicePort(port=80,target_port=int(servicePort))
        V1serviceSpec = client.V1ServiceSpec(ports=[V1servicePort], selector={'k8s-app': applyName}, type="NodePort")
        V1ObjecMeta = client.V1ObjectMeta(labels={'k8s-app': applyName}, name=applyName, namespace="default")
        V1Service = client.V1Service(api_version="v1", kind="Service", spec=V1serviceSpec, metadata=V1ObjecMeta)
        k8s_api = client.CoreV1Api()
        service = k8s_api.create_namespaced_service(namespace="default", body=V1Service)
        return service
    repositoryHost = 'hub.heshidai.com'
    project=request.POST.get('project')
    imageName=request.POST.get('imageName')
    imageTag=request.POST.get('imageTag')
    applyName=request.POST.get('applyName')
    servicePort=request.POST.get('servicePort')
    config.load_kube_config()
    def generateImage(repositoryHost, imageName, imageTag):
        image = repositoryHost + '/' + imageName + ':' + imageTag
        return image

    image=generateImage(repositoryHost, imageName, imageTag)
    def createDeployment(applyName,image,servicePort):
        V1ContainerPort = client.V1ContainerPort(container_port=int(servicePort), protocol="TCP")
        V1Container = client.V1Container(
            name=applyName,
            image=image,
            ports=[V1ContainerPort]
        )
        V1PodTemplateSpec = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(containers=[V1Container]),
            metadata={"labels":{'k8s-app':applyName}}
        )
        V1beta2DeploymentSpec = client.V1beta2DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={"k8s-app": applyName}),
            template=V1PodTemplateSpec
        )
        V1ObjectMeta = client.V1ObjectMeta(
            namespace="default",
            name=applyName
        )
        V1beta2Deployment = client.V1beta2Deployment(
            spec=V1beta2DeploymentSpec,
            api_version="apps/v1beta2",
            kind="Deployment",
            metadata=V1ObjectMeta
        )
        pprint(V1beta2Deployment)
        k8s_api = client.AppsV1beta2Api()
        deployment = k8s_api.create_namespaced_deployment(
            body=V1beta2Deployment,
            namespace="default"
        )
        pprint("Deployment create. status= '%s'" % deployment)
        return deployment

    deploymentRespond=createDeployment(applyName, image, servicePort)
    serviceRespond=createService(servicePort, applyName)
    nodePort=serviceRespond.spec.ports[0].node_port

    applyInfo = {}
    applyInfo['deployName'] = applyName
    applyInfo['createDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    applyInfo['deployStatus'] = '运行中'
    applyInfo['accessAddress'] = 'http://192.168.137.50:'+str(nodePort)
    applyInfo['imageName'] = image
    return render(request, 'dashboard/kubernetes/detailDeployment.html', applyInfo)

    # aToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlci10b2tlbi1mNnBwZiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijg3YjJlZDFiLTAyMGItMTFlOC1iNzFlLTAwMTU1ZDAxZTMwMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpuYW1lc3BhY2UtY29udHJvbGxlciJ9.J_XmQj16G8V_u-F47BZpdpNUPNLTAfo-3sPLsQeNxc89b6BMvRgeM9M03PumQpkxXFOLYXaXVQhjOGVAAyGmYeYmJec2YaF3Z-RuhoGhfKUS4Cj4CILZl_l5ZtqPywu0WWMyRtIeg2swOKxzNk0otmWaFOEQp_EAXroFWkmBY9WR3f9jhlPW8FiBHoqXM8scfqYhS25vuJJqa1rK07wbkNhA2d7Q0nrylXyVg1GwuMdC9vsJj3CI4uYn1lAjji-2909gh5bBIxvt_sCM-2R1hLMooWLbbALZsdiVf9jSpLINX-BI_JRfWsVqvey5fZHOLSuZV9v7RZwdS9gQ1SESdg"
    # configuration = client.Configuration()
    # configuration.host = "https://192.168.137.50:6443"
    # configuration.verify_ssl = False
    # configuration.api_key = {"authorization": "Bearer " + aToken}
    # client.Configuration.set_default(configuration)
    # v1 = client.CoreV1Api()
    # ret = v1.list_pod_for_all_namespaces(watch=False)
    # for i in ret.items:
    #     print("%s\t%s\t%s" %
    #           (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    # return JsonResponse({"ok":ret.items})
def deployment_info(request):
    deploymentName=request.POST.get("deploymentName")
    config.load_kube_config()
    k8s_api = client.AppsV1beta2Api()
    resp=k8s_api.read_namespaced_deployment(name=deploymentName, namespace="default")
    context = {}
    context['imageName'] = resp.spec.template.spec.containers[0].image.split(':')[0]
    context['imageTag'] = resp.spec.template.spec.containers[0].image.split(':')[1]
    context['servicePort'] = resp.spec.template.spec.containers[0].ports[0].container_port
    print(context)
    # print(deploymentName)
    return JsonResponse (context)

def deploy_image_modify(request):
    deploymentName=request.POST.get('applyName')
    imageName=request.POST.get('imageName')
    imageTag=request.POST.get('imageTag')
    servicePort=request.POST.get('servicePort')
    config.load_kube_config()
    k8s_api = client.AppsV1beta2Api()
    print(servicePort)
    if servicePort == None:
        print("部署修改镜像")
        image = imageName + ':' + imageTag
        body = k8s_api.read_namespaced_deployment(name=deploymentName, namespace="default")
        body.spec.template.spec.containers[0].image = image
        servicePort=body.spec.template.spec.containers[0].ports[0].container_port
        resp=k8s_api.patch_namespaced_deployment(name=deploymentName, namespace="default", body=body)
        applyInfo = {}
        applyInfo['deployName'] = deploymentName
        applyInfo['createDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        applyInfo['deployStatus'] = '运行中'
        applyInfo['accessAddress'] = 'http://192.168.137.50:'+str(servicePort)
        applyInfo['imageName'] = image
        return render(request, 'dashboard/kubernetes/detailDeployment.html', applyInfo)
    else:
        print("部署修改端口")
        body = k8s_api.read_namespaced_deployment(name=deploymentName, namespace="default")
        body.spec.template.spec.containers[0].ports[0].container_port = int(servicePort)
        image = body.spec.template.spec.containers[0].image
        resp=k8s_api.patch_namespaced_deployment(name=deploymentName, namespace="default", body=body)
        applyInfo = {}
        applyInfo['deployName'] = deploymentName
        applyInfo['createDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        applyInfo['deployStatus'] = '运行中'
        applyInfo['accessAddress'] = 'http://192.168.137.50:'+str(servicePort)
        applyInfo['imageName'] = image
        return render(request, 'dashboard/kubernetes/detailDeployment.html', applyInfo)

def deployment_delete(request):
    if request.method == 'POST':
        deploymentName = request.POST.get("dp_name")
        namespaceName = request.POST.get("ns_name")
        serviceName = request.POST.get("dp_name")
    def delete_service(namespace, name):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        V1status=k8s_api.delete_namespaced_service(name=name, namespace=namespace)
        return V1status
    def delete_deploy(namespace, name):
        config.load_kube_config()
        k8s_api = client.AppsV1beta2Api()
        body = client.V1DeleteOptions(api_version="apps/v1beta2")
        V1status=k8s_api.delete_namespaced_deployment(body=body, name=name, namespace=namespace)
        return V1status
    deployStatus=delete_deploy(namespaceName, deploymentName)
    serviceStatus=delete_service(namespaceName, serviceName)
    data=deployStatus.status
    return JsonResponse(data, safe=False)









