from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('home/')),
    url('recipes/', include('recipes.urls')),
    url('essen/', include('menu.urls')),
    url('admin/', admin.site.urls),
    url('accounts/', include('django.contrib.auth.urls')),
    url('home/', include('home.urls')),
]
