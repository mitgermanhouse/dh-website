from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^edit_profile/$', views.EditProfileUpdateView.as_view(), name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })]

