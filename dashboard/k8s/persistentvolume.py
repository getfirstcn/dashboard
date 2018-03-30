import time
from kubernetes import client,config
from pprint import pprint
from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

class persistentvolume_list(TemplateView):
    template_name = "dashboard/kubernetes/persistentvolume.html"