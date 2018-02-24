import requests
from django.http import HttpResponse, JsonResponse

def image(request):
    project = request.POST.get('project')
    print(project,'get project')
    r = requests.get('http://hub.heshidai.com/api/search')
    repositories = r.json()['repository']
    print(repositories)
    repositoryname=[]
    for i in repositories:
        if project == i['project_name']:
            repositoryname.append(i['repository_name'])
    return JsonResponse(repositoryname,safe=False)