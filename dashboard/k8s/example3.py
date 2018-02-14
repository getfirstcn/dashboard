from kubernetes import client, config

def main():
    config.load_kube_config()
    print("Supported APIs (* is preferred version):")
    print("%-20s %s" %
          ("core", ",".join(client.CoreApi().get_api_versions().versions)))
    for api in client.ApisApi().get_api_versions().Groups:
        versions = []
        for v in api.versions:
            name = ""
            if v.version == api.preferred_version.version and len(
                api.versions
            ) > 1:
                name += "*"
            name += v.version
            versions.append(name)
        print("%-40s %s" % (api.name, ",".join(versions)))

if __name__ == '__main__':
    config.load_kube_config()
    type(client.ApisApi().get_api_versions().Groups)
    print(client.ApisApi().get_api_versions().Groups)
    # main()
