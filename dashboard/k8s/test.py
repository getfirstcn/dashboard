from kubernetes import config, client
def changeService(service, namespace, port):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        body = k8s_api.read_namespaced_service(service,namespace)
        if port != None:
            port=body.spec.ports[0].target_port
            print(port)
        else:
            print(port+"is none")
        resp = k8s_api.patch_namespaced_service(service,namespace,body)
        return resp

re=changeService('admin-base-nginx','default',8888)
print(re)