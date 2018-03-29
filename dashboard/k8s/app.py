from django.http import JsonResponse,HttpResponse
from  django.shortcuts import render
from django.views import View
from pprint import pprint
from kubernetes import config,client
import time


#labels给一个字典参数
# servicePort, targetPort, serviceProtocol是列表
def createService(port, targetPort, protocol,name,namespace,**kwargs):
    config.load_kube_config()
    ports = []
    num=0
    labels = {}
    if isinstance(protocol,str):
        ports.append(
            client.V1ServicePort(port=int(port), target_port=int(targetPort), protocol=protocol, name="port" + str(num)))
    else:
        for (source, target, Protocol) in zip(port, targetPort, protocol):
            ports.append(client.V1ServicePort(port=int(source), target_port=int(target), protocol=Protocol,name="port"+str(num)) )
            num+=1
    if isinstance(kwargs['labelKey'],list) and isinstance(kwargs['labelValue'],list):
        for (key,value) in zip(kwargs['labelKey'],kwargs['labelValue']):
            labels[key]=value
    else:
        labels[kwargs['labelKey']]=kwargs['labelValue']
    V1serviceSpec = client.V1ServiceSpec(ports=ports, selector=labels, type="NodePort")
    V1ObjecMeta = client.V1ObjectMeta(labels=labels, name=name, namespace=namespace)
    V1Service = client.V1Service(api_version="v1", kind="Service", spec=V1serviceSpec, metadata=V1ObjecMeta)
    k8s_api = client.CoreV1Api()
    # pprint(V1Service)
    service = k8s_api.create_namespaced_service(namespace=namespace, body=V1Service)
    return service

#port 是容器是服务目标端口
def createDeployment(name,namespace,image,port,protocol,**kwargs):
        print(name,namespace,image,port,protocol,kwargs)
        labels = {}
        pprint(kwargs)
        if isinstance(kwargs['labelKey'],list) and isinstance(kwargs['labelValue'],list):
            for (key, value) in zip(kwargs['labelKey'], kwargs['labelValue']):
                labels[key] = value
        else:
            labels[kwargs['labelKey']]=kwargs['labelValue']
        V1ObjectMeta = client.V1ObjectMeta(
            namespace="default",
            name=name,
            labels=labels
        )
        ports = []
        if isinstance(port,str):
            ports.append(client.V1ContainerPort(container_port=int(port), protocol=protocol))
        else:
            for (Port,Protocol) in zip(port,protocol):
                ports.append(client.V1ContainerPort(container_port=int(Port),protocol=Protocol))
        env=[]
        if 'envKay' in kwargs.keys() and 'envValue' in kwargs.keys():
            for (k,v) in zip(kwargs['envKey'],['envValue']):
                env.append(client.V1EnvVar(name=k,value=v))
        if kwargs['command']:
            command=kwargs['command']
            print('命令错误')
        else:
            command=None
        if kwargs['args']:
            args=kwargs['args']
        else:
            args=None
        V1Container = client.V1Container(
            name=name,
            image=image,
            ports=ports,
            command=command,
            args=args,
            env=env
        )
        V1PodTemplateSpec = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(containers=[V1Container]),
            metadata=V1ObjectMeta
        )
        V1beta2DeploymentSpec = client.V1beta2DeploymentSpec(
            replicas=int(kwargs['rc']),
            selector=client.V1LabelSelector(match_labels=labels),
            template=V1PodTemplateSpec
        )

        V1beta2Deployment = client.V1beta2Deployment(
            spec=V1beta2DeploymentSpec,
            # api_version="apps/v1beta2",
            kind="Deployment",
            metadata=V1ObjectMeta
        )
        pprint(V1beta2Deployment)
        config.load_kube_config()
        k8s_api = client.AppsV1beta2Api()
        deployment = k8s_api.create_namespaced_deployment(
            body=V1beta2Deployment,
            namespace=namespace
        )
        pprint("Deployment create. status= '%s'" % deployment)
        return deployment

    # deploymentRespond=createDeployment(applyName, image, servicePort)
    # serviceRespond=createService(servicePort, applyName)
    # nodePort=serviceRespond.spec.ports[0].node_port

    # applyInfo = {}
    # applyInfo['deployName'] = applyName
    # applyInfo['createDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # applyInfo['deployStatus'] = '运行中'
    # applyInfo['accessAddress'] = 'http://192.168.254.194:'+str(nodePort)
    # applyInfo['imageName'] = image
    # return render(request, 'dashboard/kubernetes/deploymentDetail.html', applyInfo)

def getDeployment(name, namespace):
        config.load_kube_config()
        k8s_api=client.AppsV1beta2Api()
        resp=k8s_api.read_namespaced_deployment(name,namespace)
        return resp
def getService(name,namespace):
    config.load_kube_config()
    k8s_api=client.CoreV1Api()
    print(name,namespace)
    resp=k8s_api.read_namespaced_service(name,namespace,exact=True)
    return resp

def list_namespace_pods(namespace, labelKey, labelValue):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        include_uninitialized = True
        if isinstance(labelKey,str) and isinstance(labelValue,str):
            labels=labelKey+'='+labelValue
        else:
            labels=labelKey[0]+'='+labelValue[0]
        v1podList = k8s_api.list_namespaced_pod(namespace, include_uninitialized=include_uninitialized,label_selector=labels)
        return v1podList


def delete_service(namespace, name):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        V1status=k8s_api.delete_namespaced_service(name=name, namespace=namespace)
        return V1status
def delete_deploy(namespace, name):
        config.load_kube_config()
        k8s_api = client.AppsV1beta2Api()
        body = client.V1DeleteOptions(api_version="apps/v1beta2",propagation_policy='Foreground')
        V1status=k8s_api.delete_namespaced_deployment(body=body, name=name, namespace=namespace)
        return V1status

def deployment_apply(request):
    def createService(servicePort,targetPort,serviceProtocol, lableKey,lableValue,applyName):
        for (source,target,protocol) in zip(servicePort,targetPort,serviceProtocol):
            V1servicePort = []
            V1servicePort.append(client.V1ServicePort(port=source, target_port=target, protocol=protocol))
        V1serviceSpec = client.V1ServiceSpec(ports=V1servicePort, selector={'k8s-app': applyName}, type="NodePort")
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
    applyInfo['accessAddress'] = 'http://192.168.254.194:'+str(nodePort)
    applyInfo['imageName'] = image
    return render(request, 'dashboard/kubernetes/deploymentDetail.html', applyInfo)

class  app_add(View):
    def get(self,request,*args,**kwargs):
        return render(request,template_name='dashboard/kubernetes/appAdd.html')
    def post(self,request,*args,**kwargs):
        app=request.POST.get("app")
        image=request.POST.get("image")
        rc=request.POST.get("rc")
        servicePort=request.POST.get("servicePort")
        targetPort=request.POST.get("targetPort")
        serviceProtocol=request.POST.get("serviceProtocol")
        description=request.POST.get("description")
        labelKey=request.POST.get("labelKey")
        labelValue=request.POST.get("labelValue")
        print('lalllllllllll',labelKey,labelValue)
        envKey=request.POST.get("envKey")
        envValue=request.POST.get("envValue")
        command=request.POST.get("command")
        args=request.POST.get("args")
        pprint(request.POST.get)
        service=createService(port=servicePort, targetPort=targetPort, protocol=serviceProtocol, labelKey=labelKey,labelValue=labelValue, name=app, namespace="default")
        deployment=createDeployment(name=app, namespace="default", image=image, port=targetPort, protocol=serviceProtocol,
                                    envKey=envKey, envValue=envValue,
                                    labelKey=labelKey, labelValue=labelValue,
                                    rc=rc, command=command, args=args)
        podslist=list_namespace_pods(namespace='default',labelKey=labelKey,labelValue=labelValue)
        return render(request,template_name='dashboard/kubernetes/application.html',context={"service":service,"deployment":deployment, 'podlist':podslist.items})

class application(View):
    def get(self,request,*args,**kwargs):
        config.load_kube_config()
        k8s_api = client.AppsV1beta2Api()
        deployments = k8s_api.list_deployment_for_all_namespaces().items
        return render(request,template_name='dashboard/kubernetes/applications.html',context={"deployments":deployments})
    def post(self,request):
        return

class application_detail(View):
    def get(self,request):
        name=request.GET.get('name')
        namespace=request.GET.get('namespace')
        deployment=getDeployment(name,namespace)
        service=getService(name,namespace)
        for key in deployment.metadata.labels:
            labelKey=key
            labelValue=deployment.metadata.labels[key]
            break
        podlist=list_namespace_pods(namespace,labelKey,labelValue)
        return render(request,template_name='dashboard/kubernetes/application.html',context={'deployment':deployment,'service':service,'podlist':podlist.items})

class application_delete(View):
    def post(self,request):
        name=request.POST.get('name')
        namespace=request.POST.get('namespace')
        d1status=delete_deploy(namespace=namespace,name=name)
        print("deployment status",d1status)
        s1status=delete_service(namespace=namespace,name=name)
        print("service status",s1status)
        return HttpResponse(s1status.to_dict())


if __name__=='__main__':
    pass




