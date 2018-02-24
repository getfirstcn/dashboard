from django.http import JsonResponse
def app_name(request):
    image = request.POST.get('image')
    userName = request.user.username
    print(userName)
    name = userName+'-'+image.replace('/','-')
    print(name)
    return JsonResponse(name,safe=False)