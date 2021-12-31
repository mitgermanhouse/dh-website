from django.conf.urls import url

from . import auth

app_name = 'mit'
urlpatterns = [
    url(r'^auth/', auth.kerb_login, name='auth')
]
