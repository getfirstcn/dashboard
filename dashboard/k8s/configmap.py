import time
from kubernetes import client,config
from pprint import pprint
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

class configmaps(View):
    def get(self,request):
        config.load_kube_config()
        api=client.CoreV1Api()
        configmaps=api.list_config_map_for_all_namespaces().items
        print(configmaps)
        return render(request,template_name='dashboard/kubernetes/configmaps.html',context={"configmaps":configmaps})

class configmap_detail(View):
    def get(self,request):
        name=request.GET.get('name')
        namespace=request.GET.get('namespace')
        config.load_kube_config()
        api=client.CoreV1Api()
        configmap=api.read_namespaced_config_map(name,namespace).to_dict()
        pprint(configmap)
        return render(request,template_name='dashboard/kubernetes/configmap.html',context={'configmap':configmap})