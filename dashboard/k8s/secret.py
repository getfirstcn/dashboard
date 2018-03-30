import time
from kubernetes import client,config
from pprint import pprint
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

class cecrets(View):
    def get(self,request):
        config.load_kube_config()
        api=client.CoreV1Api()
        secrets=api.list_secret_for_all_namespaces().items
        print(secrets)
        return render(request,template_name='dashboard/kubernetes/secrets.html',context={"secrets":secrets})

class secret_detail(View):
    def post(self,request):
        name=request.POST.get('name')
        namespace=request.POST.get('namespace')
        print(namespace,name)
        api=client.CoreV1Api()
        secret=api.read_namespaced_secret(name=name,namespace=namespace).to_dict()
        pprint(secret)
        return render(request,template_name='dashboard/kubernetes/secret.html',context={'secret':secret})
