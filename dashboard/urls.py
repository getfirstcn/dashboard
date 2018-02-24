from django.urls import path
from . import views
from . import repositories
from .k8s import deployment_apply, deployment_delete, deployment_change, deployment_detail



urlpatterns = [
    path('login/', views.login),
    path('monitor/', views.monitor),
    path('pods/', views.pods_list),
    path('deployments/', views.deployments_list),
    path('deployment/create/', deployment_apply),
    path('deployment/delete/', deployment_delete),
    path('deployment/change/', deployment_change),
    path('deployment/detail/', deployment_detail),
    path('services/', views.services_list),
    path('links/', views.links_list),
    path('deployment/form/', views.deployment_form),
    path('upload/', views.upload),
    path('project/', repositories.project),
    path('image/', repositories.image),
    path('tag/', repositories.tag),
    path('app/name/', repositories.app_name),
    path('', views.index),
]