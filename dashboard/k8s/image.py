import requests
from django.http import  HttpResponse, JsonResponse

def get_project(request):
    r = requests.get('http://hub.heshidai.com/api/search')
    projects = r.json()['project']
    # repositories = r.json()['repository']
    return JsonResponse(projects, safe=False)
def get_image(request):
    projectName=request.POST.get('projectName')
    r = requests.get('http://hub.heshidai.com/api/search')
    # projects = r.json()['project']
    repositories = r.json()['repository']
    repositoryName=[]
    for repository in repositories:
        if repository['project_name'] == projectName:
            repositoryName.append(repository['repository_name'])
    return JsonResponse(repositoryName, safe=False)

def get_tag(request):
    imageName=request.POST.get('imageName')
    print(imageName)
    image_url="http://hub.heshidai.com/api/repositories/" + imageName + "/tags?detail=1"
    r=requests.get(image_url)
    tags=[]
    for image in r.json():
        tags.append(image['tag'])
    return JsonResponse(tags, safe=False)

