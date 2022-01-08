from django.urls import include, path, register_converter
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponseRedirect

from essen.converters import DateConverter

register_converter(DateConverter, 'y-m-d')

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('home/')),
    path('recipes/', include('recipes.urls')),
    path('menu/', include('menu.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', include('home.urls')),
    path('mit/', include('mit.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>/', serve, {
            'document_root': settings.MEDIA_ROOT,
        })]