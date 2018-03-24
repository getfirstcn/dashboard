import time
from kubernetes import client,config
from pprint import pprint
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

class list_namespaces(View):
    def get(self,request):
        print("开始")
        config.load_kube_config()
        api=client.CoreV1Api()
        namespaces=api.list_namespace().items
        print(namespaces)
        return render(request,template_name='dashboard/kubernetes/namespaces.html',context={'namespaces': namespaces})
        # return HttpResponse('ok')

class namespace_detail(View):
    def get(self,request):
        name=request.GET.get('name')
        config.load_kube_config()
        api=client.CoreV1Api()
        namespace=api.read_namespace(name=name)
        pprint(namespace)
        return render(request,template_name='dashboard/kubernetes/namespace.html',context={'namespace':namespace.to_dict()})

class list_event_all(View):
    def post(self,request):
        config.load_kube_config()
        api=client.CoreV1Api()
        events=api.list_event_for_all_namespaces().items
        # print(events)
        return render(request,template_name='dashboard/tables/events.html',context={'events':events})
    def get(self,request):
        config.load_kube_config()
        api=client.CoreV1Api()
        events=api.list_event_for_all_namespaces().items
        # print(events)
        return render(request,template_name='dashboard/kubernetes/events.html',context={'events':events})



if __name__=='__main__':
    def get():
        config.load_kube_config()
        api=client.CoreV1Api()
        ns=api.list_namespace()
        print(ns)
    get()