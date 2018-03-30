from django.http import JsonResponse,HttpResponse
from  django.shortcuts import render
from pprint import pprint
from kubernetes import config,client
from django.views import View
import json
from dateutil.tz import tzutc,tzlocal
from datetime import datetime

def list_namespace_pods(namespace,label_selector):
    config.load_kube_config()
    k8s_api=client.CoreV1Api()
    include_uninitialized = True
    v1podList=k8s_api.list_namespaced_pod(namespace,include_uninitialized=include_uninitialized,label_selector=label_selector)
    return v1podList

class service_modify(View):
    def post(self,request):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        name = request.POST.get("name")
        namespace = request.POST.get("namespace")
        print(name, namespace)
        resp = k8s_api.read_namespaced_service(name, namespace, exact=True)
        resp.metadata.creation_timestamp=resp.metadata.creation_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return JsonResponse(resp.to_str(),safe=False)


class service_detail(View):
    def post(self,request):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        name = request.POST.get("name")
        namespace = request.POST.get("namespace")
        print(name, namespace)
        resp = k8s_api.read_namespaced_service(name, namespace, exact=True)
        pprint(resp)
        label_selector = ''
        for k, v in resp.spec.selector.items():
            label_selector += k + '=' + v
        print(label_selector)
        podlist = list_namespace_pods(namespace, label_selector).items
        print(podlist)
        return render(request, 'dashboard/kubernetes/serviceDetail.html',context={'service': resp.to_dict(), 'podlist': podlist})


def service_delete(request):
    config.load_kube_config()
    k8s_api=client.CoreV1Api()
    name=request.POST.get("name")
    namespace=request.POST.get("namespace")
    resp=k8s_api.delete_namespaced_service(name,namespace)
    pprint(resp)
    return JsonResponse(resp.to_dict())

class service_update(View):
    def post(self,request):
        value=request.POST.get('value')
        valueDict=eval(value)
        name=valueDict['metadata']['name']
        namespace=valueDict['metadata']['namespace']
        config.load_kube_config()
        api=client.CoreV1Api()
        body=api.read_namespaced_service(name=name,namespace=namespace)
        body.metadata.labels=valueDict['metadata']['labels']
        body.metadata.name=valueDict['metadata']['name']
        body.spec.ports[0].port=valueDict['spec']['ports'][0]['port']
        body.spec.ports[0].target_port=valueDict['spec']['ports'][0]['target_port']
        body.spec.ports[0].protocol=valueDict['spec']['ports'][0]['protocol']
        body.spec.selector=valueDict['spec']['selector']
        body.spec.type=valueDict['spec']['type']
        rs=api.replace_namespaced_service(name=name,namespace=namespace,body=body).to_dict()
        return JsonResponse('rs',safe=False)


if __name__ == "__main__":
    label_selector = 'k8s-app=kubernetes-dashboard,pod-template-hash=4013036880'
    resp=list_namespace_pods("kube-system",label_selector)
    pprint(resp)
