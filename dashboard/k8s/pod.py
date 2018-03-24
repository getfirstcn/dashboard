from django.http import JsonResponse,HttpResponse
from  django.shortcuts import render
from django.views import View
from pprint import pprint
from kubernetes import config,client

def pod_detail(request):
    podName=request.GET.get('name')
    namespace=request.GET.get('namespace')
    # print('podNma:%s,namespace:%s'% podName,namespace)
    resp=podStatus(podName,namespace).to_dict()
    pprint(resp)
    return render(request,template_name='dashboard/kubernetes/podDetail.html',context=resp)
def podStatus(name,namespace):
        config.load_kube_config()
        k8s_api=client.CoreV1Api()
        V1pod=k8s_api.read_namespaced_pod_status(name=name,namespace=namespace)
        return V1pod
def pod_delete(request):
    name=request.POST.get("name")
    namespace=request.POST.get("namespace")
    config.load_kube_config()
    k8s_api=client.CoreV1Api()
    body=client.V1DeleteOptions()
    resp=k8s_api.delete_namespaced_pod(name,namespace,body)
    print(resp)
    return JsonResponse(True,safe=False)

class get_pod_log(View):
    def post(self,request,*args, **kwargs):
        name=request.POST.get('name')
        namespace=request.POST.get('namespace')
        print(namespace,name)
        config.load_kube_config()
        api=client.CoreV1Api()
        log=api.read_namespaced_pod_log(name,namespace)
        return JsonResponse(log,safe=False)

class get_pod_event(View):
    def post(self,request):
        name=request.POST.get('name')
        namespace=request.POST.get('namespace')
        field="involvedObject.name="+name
        print(namespace,name)
        config.load_kube_config()
        api=client.CoreV1Api()
        events=api.list_namespaced_event(namespace=namespace,field_selector=field).items
        print(events)
        # return JsonResponse({'events':events})
        return render(request,template_name='dashboard/tables/event.html',context={'events':events})


if __name__=='__main__':
    name = 'test-describe-6b847c56b4-7ns96'
    namespace = 'default'
    # field = "involvedObject.name=" + name
    # config.load_kube_config()
    # api = client.CoreV1Api()
    # log = api.list_namespaced_event(namespace=namespace,field_selector=field).items
    # log = api.read_namespaced_pod_(name, namespace)
    podlog=get_pod_event()
    log=podlog.post(name=name,namespace=namespace)
    # for i in log:
    #     print(i)
    #     print('------------------------------------------------------------------------------------')