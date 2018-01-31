from kubernetes import client, config
import urllib3

# urllib3.util.make_hearders()

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_service_for_all_namespaces(watch=False).items
    print(type(ret))
    print(type(ret.__dict__))
    for key in ret.__dict__:
        print(key)
    # for i in ret.items:
    #     print("%s\t%s\t%s\t" %
    #           (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

if __name__ == '__main__':
    main()
