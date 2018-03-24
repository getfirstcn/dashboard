import time
from kubernetes import client,config
from pprint import pprint
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

class nodes(View):
    def get(self,request):
        config.load_kube_config()
        api=client.CoreV1Api()
        nodes=api.list_node().items
        pprint(nodes)
        return render(request,template_name='dashboard/kubernetes/nodes.html',context={'nodes':nodes})

class node_detail(View):
    def get(self,request):
        name=request.GET.get('name')
        config.load_kube_config()
        api=client.CoreV1Api()
        node=api.read_node(name).to_dict()
        pprint(node)
        return render(request,template_name='dashboard/kubernetes/node.html',context={'node':node})