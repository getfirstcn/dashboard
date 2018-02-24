from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from kubernetes import client,config
from pprint import pprint
import time


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
    return render(request, 'dashboard/kubernetes/deploymentDetail.html', applyInfo)

def deployment_delete(request):
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
    deploy = request.POST.get('deploy')
    nameSpace = request.POST.get('namespace')
    print(request.method)
    print(deploy,nameSpace)
    config.load_kube_config
    resultDeploy=delete_deploy(nameSpace,deploy)
    resultService=delete_service(nameSpace,deploy)
    print(resultDeploy,resultService)
    return JsonResponse('ok',safe=False)

def deployment_change(request):
    def changeDeployment(deployment,namespace,image,port):    
        config.load_kube_config()
        k8s_api = client.AppsV1beta2Api()
        body = k8s_api.read_namespaced_deployment(name=deployment, namespace=namespace)
        if image != None:
            body.spec.template.spec.containers[0].image = image
        else:
            print(image+"is none")
        if port != None:
            body.spec.template.spec.containers[0].ports[0].container_port = int(port)
        else:
            print(port+"is none")
        resp=k8s_api.patch_namespaced_deployment(name=deployment, namespace=namespace, body=body)
        return resp
    def changeService(service, namespace, port):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        body = k8s_api.read_namespaced_service(service,namespace)
        if port != None:
            body.spec.ports[0].target_port=int(port)
        else:
            print(port+"is none")
        resp = k8s_api.patch_namespaced_service(service,namespace,body)
        return resp
    def generateImage(repositoryHost, imageName, imageTag):
        image = repositoryHost + '/' + imageName + ':' + imageTag
        return image

    repositoryHost = 'hub.heshidai.com'
    applyName=request.POST.get('applyName')
    namespace=request.POST.get('namespace')
    imageName=request.POST.get('imageName')
    imageTag=request.POST.get('imageTag')
    servicePort=request.POST.get('servicePort')
    image=generateImage(repositoryHost, imageName, imageTag)
    deploymentRespond=changeDeployment(applyName, namespace, image, servicePort)
    serviceRespond=changeService(applyName, namespace, servicePort)
    nodePort=serviceRespond.spec.ports[0].node_port
    applyInfo = {}
    applyInfo['deployName'] = applyName
    applyInfo['createDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    applyInfo['deployStatus'] = '运行中'
    applyInfo['accessAddress'] = 'http://192.168.137.50:'+str(nodePort)
    applyInfo['imageName'] = image
    return render(request, 'dashboard/kubernetes/deploymentDetail.html', applyInfo)

def deployment_detail(request):
    def getDeployment(name, namespace):
        config.load_kube_config()
        k8s_api=client.AppsV1beta2Api()
        resp=k8s_api.read_namespaced_deployment(name,namespace)
        return resp

    deploymenyName=request.GET.get('name')
    print(deploymenyName)
    namespace=request.GET.get('namespace')
    deployInfo=getDeployment(deploymenyName,namespace)
    pprint(deployInfo.to_dict())
    return render(request,'dashboard/kubernetes/appDetail.html',deployInfo.to_dict())

