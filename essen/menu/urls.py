from django.conf.urls import url

from . import views

app_name = 'menu'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<date>[0-9]+[\/][0-9]+[\/][0-9]+)/$', views.index, name='index'),
    url(r'^add_menu/$', views.add_menu, name='add_menu'),
    url(r'^submit_menu/$', views.submit_menu, name='submit_menu'),
    url(r'^display_meal/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='display_meal'),
    url(r'^add_lateplate/(?P<pk>[0-9]+)/$', views.add_lateplate, name='add_lateplate'),
    url(r'^shopper/(?P<pk>[0-9]+)/$', views.shopper, name='shopper')
]

