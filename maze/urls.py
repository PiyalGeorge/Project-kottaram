from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import homeview

urlpatterns = [

    url(r'^$', homeview, name='home'),
    url(r'^account/', include('accounts.urls', namespace="account")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
]
