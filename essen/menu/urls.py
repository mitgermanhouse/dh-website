from django.urls import path, re_path

from . import views

app_name = 'menu'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<date>[0-9]+[\/][0-9]+[\/][0-9]+)/$', views.index, name='index'),
    re_path(r'^add_menu/$', views.add_menu, name='add_menu'),
    re_path(r'^submit_menu/$', views.submit_menu, name='submit_menu'),
    re_path(r'^display_meal/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='display_meal'),
    re_path(r'^add_lateplate/(?P<pk>[0-9]+)/$', views.add_lateplate, name='add_lateplate'),
    re_path(r'^remove_lateplate/(?P<pk>[0-9]+)/$', views.remove_lateplate, name='remove_lateplate'),
    re_path(r'^shopper/(?P<pk>[0-9]+)/$', views.shopper, name='shopper'),
    re_path(r'^auto_lateplates/$', views.AutoLatePlates.as_view(), name='auto_lateplates'),
    re_path(r'^submit_auto_lateplates/$', views.submit_auto_lateplates, name="submit_auto_lateplates"),
    re_path(r'^remove_auto_lateplates/(?P<pk>[0-9]+)/$', views.remove_auto_lateplates, name="remove_auto_lateplates"),
    re_path(r'^ingredient_info/(?P<ing>[0-9]+)[\/](?P<menu>[0-9]+)/$', views.ingredient_info, name='ingredient_info'),
]

