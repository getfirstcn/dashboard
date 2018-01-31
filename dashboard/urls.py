from django.urls import path, re_path
from . import  views
from . import user, server
from dashboard.user import group
from . import k8s

urlpatterns = [
    path('server/add/', server.Addserver.as_view()),
    path('server/list/', server.GroupList.as_view()),
    path('group/usergroup/', group.UserGroup.as_view()),
    path('group/per/', group.PermissionList.as_view()),
    path('group/list/', group.GroupListView.as_view()),
    path('group/', group.GroupView.as_view()),
    path('user/modify/', user.Modify_status.as_view(), name='usermodify'),
    path('user/userlist/', user.LW.as_view(), name='userlist'),
    re_path('dashboard/select/(?P<types>\w*)/', k8s.SelectType.as_view()),
    path('dashboard/service/', k8s.service_list.as_view(), name='servicelist'),
    path('dashboard/deploylist/', k8s.deploy_list.as_view(), name='deploylist'),
    path('dashboard/podlist/', k8s.pod_list, name='podslist'),
    path('dashboard/nslist/', k8s.ns_list.as_view(), name='nslist'),
    path('dashboard/', views.IndexView.as_view(), name='index'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('user/userlist/', user.LW.as_view()),
    path('user/modify/', user.Modify_status.as_view()),
    path('user/modp/', user.ModifyDepartmentView.as_view()),
    path('user/mp/', user.ModifyDepartmentView.as_view()),
    path('permissions/none/', views.permit),
    path('', views.IndexView.as_view(), name='default')
]