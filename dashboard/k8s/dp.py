from os import path
import yaml
from kubernetes import client, config

def create_deployment_object(images, tags, rc, envs):
    if '/'  in images:
        name = images.split('/')[-1]
    else:
        name = images
    image = images+':'+tags
    container = client.V1Container(
        name=name,
        image='hub.heishidai.com'+image,
        env=[{'name': 'CONFIG_ENV', 'value': envs}],
        resources=client.V1ResourceRequirements(requests={'cpu':'1000m', 'memory': '1024m'}, limits={'cpu': '1500m', 'memory': '2048m'})
    )
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={'app': name}),
        spec=client.V1PodSpec(containers=[container],
                              image_pull_secrets=[{'name': 'regssecret'}])
    )
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=rc,
        template=template
    )
    deployment = client.ExtensionsV1beta1Deployment(
        api_version='extensions/v1beta1',
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )
    return deployment
def create_deployment(api_instence, deployment, ns):
    api_response = api_instence.create_namespaced_deployment(
        body=deployment,
        namespace=ns
    )
    print('Deployment created, status="%s"' % str(api_response.status))
    return api_response.status

def update_deployment(api_instence, deployment, images):
    if '/' in images:
        name = images.split('/')[-1]
    else:
        name = images
    deployment.spece.template.spec.containers[0].image = name
    api_response = api_instence.patch_namespaced_deployment(
        name=name,
        namespace='default',
        body=deployment
    )
    print("Deployment updated. status='s%'" % str(api_response.status))

def delete_deployment(api_instance, ns, images):
    if '/' in images:
        name = images.split('/')[-1]
    else:
        name = images
    api_response = api_instance.delete_namespaced_deployment(
        name=name,
        namespace=ns,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5
        )
    )
    print("deployment deleted. status='%s'" % str(api_response.status))

def main():
    config.load_kube_config()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()

    ns = 'bb'
    msg = 'base/ngin'
    tags = '1.7.9'
    rc = 1
    env= 'test'

    deployment = create_deployment_object(tags=tags, images=msg, envs=env, rc=rc)
    #delete_deployment(extensions_v1beta1, ns=ns, images=msg)

if __name__ == '__main__':
    main()
