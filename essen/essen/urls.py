from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url('recipes/', include('recipes.urls')),
    url('essen/', include('menu.urls')),
    url('admin/', admin.site.urls),
    url('accounts/', include('django.contrib.auth.urls')),
]
