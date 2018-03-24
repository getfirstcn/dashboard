from django.urls import path
from . import views
from . import repositories
from .k8s import deployment_apply, deployment_delete, deployment_change, deployment_detail
from .account import account_login,account_logout
from .k8s.pod import pod_detail,pod_delete,get_pod_log,get_pod_event
from .k8s.service import service_detail,service_delete
from .k8s.app import app_add,application,application_detail,application_delete
from .k8s import namespace
from .k8s import node,configmap,secret,event,editor,service
from .k8s import deployment



urlpatterns = [
    path('test/',views.test),
    path('editor/',editor.service_editer.as_view()),
    path('namespaces/',namespace.list_namespaces.as_view()),
    path('namespace/detail/',namespace.namespace_detail.as_view()),
    path('namespace/event/',namespace.list_event_all.as_view()),
    path('events/',namespace.list_event_all.as_view()),
    path('event/detail/',event.event_detail.as_view()),
    # path('event/detail/',event.get),
    path('nodes/',node.nodes.as_view()),
    path('node/detail/',node.node_detail.as_view()),
    path('configmaps/',configmap.configmaps.as_view()),
    path('configmap/detail/',configmap.configmap_detail.as_view()),
    path('secrets/',secret.cecrets.as_view()),
    path('secret/detail/',secret.secret_detail.as_view()),
    path('accounts/login/', account_login),
    path('login/', views.login),
    path('logout/', account_logout),
    path('monitor/', views.monitor),
    path('pods/', views.pods_list),
    path('pod/detail/',pod_detail),
    path('pod/delete/',pod_delete),
    path('pod/log/',get_pod_log.as_view()),
    path('pod/event/',get_pod_event.as_view()),
    path('applications/', application.as_view()),
    path('application/detail/', application_detail.as_view()),
    path('application/delete/', application_delete.as_view()),
    path('deployments/', views.deployments_list),
    path('deployment/create/', deployment_apply),
    path('deployment/delete/', deployment_delete),
    path('deployment/change/', deployment_change),
    path('deployment/detail/', deployment_detail),
    path('deployment/read/', deployment.deployment_read.as_view()),
    path('deployment/modify/', deployment.deployment_modify.as_view()),
    path('services/', views.services_list),
    path('service/detail/', service_detail.as_view()),
    path('service/delete/', service_delete),
    path('service/update/', service.service_update.as_view()),
    path('links/', views.links_list),
    path('deployment/form/', views.deployment_form),
    path('upload/', views.upload),
    path('project/', repositories.project),
    path('image/', repositories.image),
    path('tag/', repositories.tag),
    path('app/name/', repositories.app_name),
    path('app/add/', app_add.as_view(),name='app-add'),
    path('', views.index),
]