from kubernetes import client, config
from pprint import pprint
from kubernetes.client.rest import ApiException
from os import path
import yaml

def main():
    #aToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlci10b2tlbi1mNnBwZiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijg3YjJlZDFiLTAyMGItMTFlOC1iNzFlLTAwMTU1ZDAxZTMwMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpuYW1lc3BhY2UtY29udHJvbGxlciJ9.J_XmQj16G8V_u-F47BZpdpNUPNLTAfo-3sPLsQeNxc89b6BMvRgeM9M03PumQpkxXFOLYXaXVQhjOGVAAyGmYeYmJec2YaF3Z-RuhoGhfKUS4Cj4CILZl_l5ZtqPywu0WWMyRtIeg2swOKxzNk0otmWaFOEQp_EAXroFWkmBY9WR3f9jhlPW8FiBHoqXM8scfqYhS25vuJJqa1rK07wbkNhA2d7Q0nrylXyVg1GwuMdC9vsJj3CI4uYn1lAjji-2909gh5bBIxvt_sCM-2R1hLMooWLbbALZsdiVf9jSpLINX-BI_JRfWsVqvey5fZHOLSuZV9v7RZwdS9gQ1SESdg"
    config.load_kube_config()
    #configuration = client.Configuration()
    # Specify the endpoint of your Kube cluster
    #configuration.host = "https://192.168.137.50:6443"

    #configuration.verify_ssl = False

    #configuration.api_key["authorization"] = "Bearer "+aToken

    api_instance = client.AppsV1beta1Api()
    image="nginx"
    namespace = "default"
    containers = client.V1Container(name="nginx", image=image, ports=[client.V1ContainerPort(container_port=80)])
    template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"app":"nginx"}), spec=client.V1PodSpec(containers=[containers]))
    deploymentSpec = client.V1beta1DeploymentSpec(replicas=1, template=template)
    deployment = client.V1beta1Deployment(metadata=client.V1ObjectMeta(name="nginx"), kind="Deployment", spec=deploymentSpec, api_version="apps/v1beta1")

    # body = client.AppsV1beta2Deployment()
    try:
        api_response = api_instance.create_namespaced_deployment(namespace,body=deployment)
        pprint(api_response)
    except ApiException as e:
        print("创建部署异常：create_namespaced_deployment: %s\n" % e)

def second():
    config.load_kube_config()
    # configuration = client.Configuration()
    # configuration.host = "https://192.168.137.50:6443"
    # configuration.verify_ssl = False
    # client.Configuration.set_default(configuration)
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    print(type(ret.items))
    for i in ret.items:
        print(type(i))
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def three():
    config.load_kube_config()
    api_instance = client.ExtensionsV1beta1Api()
    container = client.V1Container(
        name="nginx",
        image="nginx",
        ports=[client.V1ContainerPort(container_port=80)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=3,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="nginx"),
        spec=spec)
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))

def four():
    # aToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlci10b2tlbi1mNnBwZiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijg3YjJlZDFiLTAyMGItMTFlOC1iNzFlLTAwMTU1ZDAxZTMwMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpuYW1lc3BhY2UtY29udHJvbGxlciJ9.J_XmQj16G8V_u-F47BZpdpNUPNLTAfo-3sPLsQeNxc89b6BMvRgeM9M03PumQpkxXFOLYXaXVQhjOGVAAyGmYeYmJec2YaF3Z-RuhoGhfKUS4Cj4CILZl_l5ZtqPywu0WWMyRtIeg2swOKxzNk0otmWaFOEQp_EAXroFWkmBY9WR3f9jhlPW8FiBHoqXM8scfqYhS25vuJJqa1rK07wbkNhA2d7Q0nrylXyVg1GwuMdC9vsJj3CI4uYn1lAjji-2909gh5bBIxvt_sCM-2R1hLMooWLbbALZsdiVf9jSpLINX-BI_JRfWsVqvey5fZHOLSuZV9v7RZwdS9gQ1SESdg"
    conf=config.load_kube_config()
    print(conf)
    exit()
    # configuration = client.Configuration()
    # configuration.host = "https://192.168.137.50:6443"
    #
    # configuration.verify_ssl = False
    #
    # configuration.api_key["authorization"] = "Bearer "+aToken
    # client.Configuration.set_default(configuration)

    with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
        dep = yaml.load(f)
        # pprint(dep)
        k8s_beta = client.AppsV1beta2Api()
        resp = k8s_beta.create_namespaced_deployment(
            body=dep,
            namespace="default"
        )
        print("Deployment create. status= '%s'" % str(resp.status))

def apiGroup():
    config.load_kube_config()
    api_instance = client.AdmissionregistrationApi()

    try:
        api_response = api_instance.get_api_group()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)

def six():
    config.load_kube_config()
    k8s_api = client.AppsV1beta2Api()
 #    deploy={'apiVersion': 'apps/v1beta2',
 # 'kind': 'Deployment',
 # 'metadata': {'labels': {'k8s-app': 'nginx'},
 #              'name': 'nginx-deployment',
 #              'namespace': 'default'},
 # 'spec': {'replicas': 1,
 #          'selector': {'matchLabels': {'k8s-app': 'nginx'}},
 #          'template': {'metadata': {'labels': {'k8s-app': 'nginx'}},
 #                       'spec': {'containers': [{'image': 'nginx',
 #                                                'name': 'nginx',
 #                                                'ports': [{'containerPort': 80,
 #                                                           'protocol': 'TCP'}]}]}}}}
 #    deploy["kind"]
    repositoryHost = ''
    project = ''
    imageName = 'nginx'
    imageTag = ''
    applyName = 'nginx'
    servicePort = 80
    containerPort = client.V1ContainerPort(container_port=80, protocol="TCP")
    container = client.V1Container(
        name="nginx",
        image="nginx",
        ports=[containerPort]
    )
    podTemplate = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(containers=[container]),
        metadata={"labels":{'k8s-app':"nginx"}}
    )
    deploymentSpec = client.V1beta2DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={"k8s-app": "nginx"}),
        template=podTemplate
    )
    deploymentObjectMeta = client.V1ObjectMeta(
        namespace="default",
        name="nginx-deploy"
    )
    deployment = client.V1beta2Deployment(
        spec=deploymentSpec,
        api_version="apps/v1beta2",
        kind="Deployment",
        metadata=deploymentObjectMeta
    )
    # pprint(deployment)


    resp = k8s_api.create_namespaced_deployment(
        body=deployment,
        namespace="default"
    )
    pprint("Deployment create. status= '%s'" % str(resp.status))

def seven():
    config.load_kube_config()
    repositoryHost = 'hub.heshidai.com'
    project='base'
    imageName='base/nginx'
    imageTag='1.9.1'
    applyName='feifei-base-nginx'
    servicePort=80
    config.load_kube_config()
    containerPort = client.V1ContainerPort(container_port=servicePort, protocol="TCP")
    container = client.V1Container(
        name=applyName,
        image=repositoryHost+'/'+imageName+':'+imageTag,
        ports=[containerPort]
    )
    podTemplate = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(containers=[container]),
        metadata={"labels":{'k8s-app':applyName}}
    )
    deploymentSpec = client.V1beta2DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={"k8s-app": applyName}),
        template=podTemplate
    )
    deploymentObjectMeta = client.V1ObjectMeta(
        namespace="default",
        name=applyName+"deploy"
    )
    deployment = client.V1beta2Deployment(
        spec=deploymentSpec,
        api_version="apps/v1beta2",
        kind="Deployment",
        metadata=deploymentObjectMeta
    )

    k8s_api = client.AppsV1beta2Api()
    resp = k8s_api.create_namespaced_deployment(
        body=deployment,
        namespace="default"
    )
    pprint("Deployment create. status= '%s'" % str(resp.status))
    print(resp)



if __name__ == '__main__':
    seven()
