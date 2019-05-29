from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^submit_profile/$', views.submit_profile, name='submit_profile'),
]

