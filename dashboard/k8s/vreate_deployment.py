from os import path
import yaml

from kubernetes import client, config

def main():
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
        dep = yaml.load(f)
        k8s_beta = client.AppsV1beta2Api()
        resp = k8s_beta.create_namespaced_deployment(
            body=dep, namespace="default"
        )
    # desp = k8s_beta.delete_namespaced_deployment(name='nginx-deployment',body=dep, namespace="default")
    print("Deployment created. status='%s'" % str(desp.status))

if __name__ == '__main__':
    main()

