import time
from kubernetes import client,config
from pprint import pprint
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

class service_editer(View):
    def post(self,request):
        pass
    def get(self,request):
        return render(request,template_name='dashboard/kubernetes/editor.html')

