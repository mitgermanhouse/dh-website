from django.urls import path

from . import auth

app_name = 'mit'
urlpatterns = [
    path('auth/', auth.kerb_login, name='auth')
]
