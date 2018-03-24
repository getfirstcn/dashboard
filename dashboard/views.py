from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from kubernetes import client, config
from . import repositories
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    return render(request, 'dashboard/index.html')

def login(request):
    return render(request, 'dashboard/login.html')

def monitor(request):
    return render(request, 'dashboard/kubernetes/monitor.html')

@login_required(login_url='/login/')
def pods_list(request):
    config.load_kube_config()
    k8s_api = client.CoreV1Api()
    pods = k8s_api.list_pod_for_all_namespaces(watch=False).items
    print(pods)
    return render(request, 'dashboard/kubernetes/pods.html', {"pods":pods})

@login_required(login_url='/login/')
def deployments_list(request):
    config.load_kube_config()
    k8s_api = client.AppsV1beta2Api()
    deployments= k8s_api.list_deployment_for_all_namespaces().items
    return render(request, 'dashboard/kubernetes/deployments.html',{"deployments":deployments})

@login_required(login_url='/login/')
def services_list(request):
    config.load_kube_config()
    k8s_api = client.CoreV1Api()
    services = k8s_api.list_service_for_all_namespaces(watch=False).items
    print(services)
    return render(request, 'dashboard/kubernetes/services.html',{"services":services})

def links_list(request):
    return render(request, 'dashboard/kubernetes/links.html')

def deployment_form(request):
    return render(request, 'dashboard/form/deploymentForm.html')
def upload(request):
    if request.method == 'GET':
        return render(request, 'dashboard/form/upload.html')
    if request.method == 'POST':
        # form = uploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        # print(dir(request.FILES))       
        # print(request.FILES,'dddddddddddddddddd')
        handle_upload_file(request.FILES['uploadFile1'])
        return HttpResponse("<h1>上传成功</h1>")
    else:
        return HttpResponse("<h1>上传不成功</h1>")

class uploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def handle_upload_file(f):
    with open('name.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def test(request):
    body=[1,2,3,4]
    return render(request,template_name='dashboard/test.html',context={"body":body})



