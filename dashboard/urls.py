from django.urls import path
from . import  views
from . import user

urlpatterns = [
    path('dashboard/', views.IndexView.as_view(), name='index'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('user/userlist/', user.LW.as_view()),
    path('', views.DefaultView.as_view(), name='default')
]