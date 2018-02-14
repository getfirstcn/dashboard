from django.urls import path, re_path
from . import  views
from . import user, server
from dashboard.user import group
from . import k8s

urlpatterns = [
    path('repository/tag/get/', k8s.image.get_tag, name='getTag'),
    path('repository/image/get/', k8s.image.get_image, name='getImage'),
    path('repository/project/get/', k8s.image.get_project, name="getProject"),
    path('server/add/', server.Addserver.as_view()),
    path('server/list/', server.GroupList.as_view()),
    path('group/usergroup/', group.UserGroup.as_view()),
    path('group/per/', group.PermissionList.as_view()),
    path('group/list/', group.GroupListView.as_view()),
    path('group/', group.GroupView.as_view()),
    path('user/modify/', user.Modify_status.as_view(), name='usermodify'),
    path('user/userlist/', user.LW.as_view(), name='userlist'),
    re_path('dashboard/select/(?P<types>\w*)/', k8s.SelectType.as_view()),
    #re_path('deploy/(?P<types>\w*)', k8s.add_mod_deploy.as_view(), name='add_deploy'),
    path('dashboard/service/', k8s.service_list.as_view(), name='servicelist'),
    path('dashboard/deploylist/', k8s.deploy_list.as_view(), name='deploylist'),
    path('dashboard/podlist/', k8s.pod_list, name='podslist'),
    path('dashboard/nslist/', k8s.ns_list.as_view(), name='nslist'),
    path('dashboard/layout/', views.layout, name='layout'),
    path('dashboard/deploy/add/', k8s.deploy_add.as_view(), name='deployadd'),
    path('dashboard/deploy/delete/', k8s.deployment_delete, name='deploydelete'),
    path('dashboard/deploy/info/', k8s.deployment_info),
    path('dashboard/deploy/image/modify/', k8s.deploy_image_modify),
    path('dashboard/deployment/', k8s.deployment_apply,name="deploymentapply"),
    path('dashboard/repository/select/', k8s.repository_select),
    path('dashboard/image/tag/get/', k8s.image_tag_get),
    path('dashboard/', views.IndexView.as_view(), name='index'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('user/userlist/', user.LW.as_view()),
    path('user/modify/', user.Modify_status.as_view()),
    path('user/modp/', user.ModifyDepartmentView.as_view()),
    path('user/mp/', user.ModifyDepartmentView.as_view()),
    path('user/current/get/',user.getCurrenUser, name="getCurrenUser"),
    path('permissions/none/', views.permit),
    path('', views.IndexView.as_view(), name='default')
]