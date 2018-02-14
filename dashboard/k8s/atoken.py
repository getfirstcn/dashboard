from kubernetes import client, config


def main():
    # Define the barer token we are going to use to authenticate.
    # See here to create the token:
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
    aToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlci10b2tlbi1mNnBwZiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijg3YjJlZDFiLTAyMGItMTFlOC1iNzFlLTAwMTU1ZDAxZTMwMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpuYW1lc3BhY2UtY29udHJvbGxlciJ9.J_XmQj16G8V_u-F47BZpdpNUPNLTAfo-3sPLsQeNxc89b6BMvRgeM9M03PumQpkxXFOLYXaXVQhjOGVAAyGmYeYmJec2YaF3Z-RuhoGhfKUS4Cj4CILZl_l5ZtqPywu0WWMyRtIeg2swOKxzNk0otmWaFOEQp_EAXroFWkmBY9WR3f9jhlPW8FiBHoqXM8scfqYhS25vuJJqa1rK07wbkNhA2d7Q0nrylXyVg1GwuMdC9vsJj3CI4uYn1lAjji-2909gh5bBIxvt_sCM-2R1hLMooWLbbALZsdiVf9jSpLINX-BI_JRfWsVqvey5fZHOLSuZV9v7RZwdS9gQ1SESdg"

    # Create a configuration object
    configuration = client.Configuration()

    # Specify the endpoint of your Kube cluster
    configuration.host = "https://192.168.137.50:6443"

    # Security part.
    # In this simple example we are not going to verify the SSL certificate of
    # the remote cluster (for simplicity reason)
    configuration.verify_ssl = False
    # Nevertheless if you want to do it you can with these 2 parameters
    # configuration.verify_ssl=True
    # ssl_ca_cert is the filepath to the file that contains the certificate.
    # configuration.ssl_ca_cert="certificate"

    configuration.api_key = {"authorization": "Bearer " + aToken}

    # Use our configuration
    client.Configuration.set_default(configuration)

    # Do calls
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    print(type(ret.items))
    for i in ret.items:
        print(type(i))
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()


