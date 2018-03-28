from kubernetes import config, client
import json
import datetime
from datetime import  datetime
from pprint import pprint
def changeService(service, namespace, port):
        config.load_kube_config()
        k8s_api = client.CoreV1Api()
        body = k8s_api.read_namespaced_service(service,namespace).to_dict()
        for key,value in body.items():
            print(key,'=',value)
        # if port != None:
        #     body['spec']['ports'][0]['target_port']=port
        #     pprint(body)
        # else:
        #     body['spec']['ports'][0]['target_port'] = port
        #     print(port+"is none")
        # resp = k8s_api.replace_namespaced_service(service,namespace,body)
        # return resp
def str_filter():
    b="{start_time': '2018-03-05T11:37:07Z'}"
    c=b.split('_')
    e=''
    for d in c:
        e+=d.capitalize()
    f=eval(e)
    pprint(f)



# re=changeService('admin-base-nginx','default',8888)

# get="{'api_version': 'v1','generation1': None,'generation2': None,'generation3': None,'generation4': None}"
# print(type(get))
# print(get)
# service = eval(get)
# print(type(service))
# print(service)

#
#
# protocol=get['serviceProtocol']
# print(isinstance(protocol,list))
if __name__=="__main__":
    # a=changeService(service='eureka-server1',namespace='default',port=9999)
    # print(a)
    # from dateutil.tz import tzutc,tzlocal
    # time=datetime(2018, 3, 14, 2, 34, 39,tzinfo=tzlocal())
    # stime=time.strftime('%Y-%m-%d %H:%M:%S')
    # print(type(stime))
    # str_filter()
    config.load_kube_config()
    name='eureka-server1-7547659986-shdn5'
    namespace='default'
    command='bash'
    # container=
    stderr = True
    stdin = True
    stdout = True
    tty=True
    api=client.CoreV1Api()
    api.connect_get_namespaced_pod_exec(name=name,namespace=namespace,command=command,stderr=True,stdin=True,stdout=True)
