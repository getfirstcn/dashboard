from kubernetes import client, config
import urllib3
import requests
import json
from pprint import pprint

# urllib3.util.make_hearders()
#
# def main():
#     config.load_kube_config()
#     v1 = client.CoreV1Api()
#     print("Listing pods with their IPs:")
#     ret = v1.list_service_for_all_namespaces(watch=False).items
#     print(type(ret))
#     print(type(ret.__dict__))
#     for key in ret.__dict__:
#         print(key)
#     # for i in ret.items:
#     #     print("%s\t%s\t%s\t" %
#     #           (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
#
# if __name__ == '__main__':
#     main()
from os import path
import yaml
from kubernetes import client, config

def create_deployment_object():
    client.V1Container(
        name="nginx",
        image='nginx',
        env=[{"name":'nginx', 'user':'wangyijie'}],
        resources=client.V1ResourceRequirements(requests={'cpu': '1000m', 'memory': '1024M'}, limits={'cpu': '1500m', 'memory': '2048M'}),
    )

def get_images():
    r = requests.get('http://hub.heshidai.com/api/search')
    # print(type(r.json()))
    # print(type(r.text))
    # re= json.load(r.json()
    # for i in r.json()['project']:
    #     print(i)
    # print(type(r.json()['repositorie']))
    for i in r.json()['repository']:
        print(i)

def repository_select():
    config.load_kube_config()
    repo={'project': 'base'}
    project= repo['project']
    r = requests.get('http://hub.heshidai.com/api/search')
    repositories = r.json()['repository']
    repositoryname=[]
    for i in repositories:
        if project in i['repository_name']:
            repositoryname.append(i['repository_name'])
    print(repositoryname)

def createService(applyName,targetPort):
        config.load_kube_config()
        V1servicePort = client.V1ServicePort(port=80,target_port=targetPort,protocol="TCP")
        V1serviceSpec = client.V1ServiceSpec(ports=[V1servicePort], selector={'k8s-app': applyName})
        V1ObjecMeta = client.V1ObjectMeta(labels={'k8s-app': applyName}, name=applyName, namespace="default")
        V1Service = client.V1Service(api_version="v1", kind="Service", spec=V1serviceSpec, metadata=V1ObjecMeta)
        # pprint(V1Service)
        k8s_api = client.CoreV1Api()
        service = k8s_api.create_namespaced_service(namespace="default", body=V1Service)
        return service
def getService(applyName):
    config.load_kube_config()
    k8s_api=client.CoreV1Api()
    service=k8s_api.read_namespaced_service(name=applyName, namespace="default")
    print(service)
    nodePort=service.spec.ports[0].node_port
    print('======================',nodePort)

def patchService(applyName):
    config.load_kube_config()
    k8s_api=client.CoreV1Api()
    body=k8s_api.read_namespaced_service(name=applyName, namespace="default")
    body.spec.type="NodePort"
    service=k8s_api.patch_namespaced_service(name=applyName, namespace="default", body=body)
    pprint(service)




if __name__ == "__main__":
    # get_images()
    # patchService('wangyijie-base-nginxdeploy')
    getService('wangyijie-base-nginxdeploy')