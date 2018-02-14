from kubernetes import client,config
from kubernetes.client import configuration
from pick import pick

def main():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    contexts = [context['name'] for context in contexts]
    active_context = contexts.index(active_context['name'])
    option, _ = pick(contexts, title="pick the context to load", default_index=active_context)

    config.load_kube_config(context=option)

    print("Active host is %s" % configuration.host)

    v1 = client.Corev1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for item in ret.items:
        print("%s\t%s\t%s" %
              (item.status.pod_ip,
               item.metadata.namespace,
               item.metadata.name))

if __name__ == '__main__':
    main()