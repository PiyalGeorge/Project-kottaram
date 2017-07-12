from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'login/$', views.loginview, name='login'),
    url(r'logout/$', views.logoutview, name='logout'),

]