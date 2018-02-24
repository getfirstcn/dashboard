import requests
from django.http import HttpResponse, JsonResponse

def project(request):
    r = requests.get('http://hub.heshidai.com/api/search')
    project = r.json()['project']
    return JsonResponse(project,safe=False)
