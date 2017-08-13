from django.conf.urls import url

from . import views
from accounts.views import LoginView

urlpatterns = [

    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', views.logoutview, name='logout'),
    url(r'test/$', views.testview, name='test'),

]