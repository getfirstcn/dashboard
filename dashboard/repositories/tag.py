import requests
from django.http import HttpResponse, JsonResponse

def tag(request):
    image = request.POST.get('image')
    print(image)
    url="http://hub.heshidai.com/api/repositories/" + image + "/tags?detail=1"
    r = requests.get(url)
    tags=[]
    for i in r.json():
        tags.append(i['tag'])
    return JsonResponse(tags,safe=False)