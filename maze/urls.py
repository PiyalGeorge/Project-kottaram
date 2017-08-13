from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from accounts.views import homeview


urlpatterns = [

    url(r'^$', homeview, name='home'),
    url(r'^account/', include('accounts.urls', namespace="account")),
    url(r'^accounts/social/login/error/$', RedirectView.as_view(url='/accounts/login/')),
    url(r'^accounts/social/login/cancelled/$', RedirectView.as_view(url='/accounts/login/')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
