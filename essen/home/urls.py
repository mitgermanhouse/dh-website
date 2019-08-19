from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^submit_profile/$', views.submit_profile, name='submit_profile'),
]
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })]

