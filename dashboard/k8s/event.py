import time
from kubernetes import client,config
from pprint import pprint
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

class event_detail(View):
    def get(self,request):
        name=request.GET.get('name')
        namespace=request.GET.get('namespace')
        print(name)
        config.load_kube_config()
        api=client.CoreV1Api()
        event=api.read_namespaced_event(name=name,namespace=namespace).to_dict()
        pprint(event)
        # return HttpResponse(event)
        return JsonResponse(event)

    def post(self,request):
        name=request.POST.get('name')
        namespace=request.POST.get('namespace')
        print(name)
        config.load_kube_config()
        api=client.CoreV1Api()
        event=api.read_namespaced_event(name=name,namespace=namespace).to_dict()
        pprint(event)
        return JsonResponse(event,safe=False)

def get(request):
        name=request.GET.get('name')
        namespace=request.GET.get('namespace')
        print(name)
        config.load_kube_config()
        api=client.CoreV1Api()
        event=api.read_namespaced_event(name=name,namespace=namespace).to_dict()
        pprint(event)
        # return JsonResponse(event,safe=False)
        return HttpResponse(event)

