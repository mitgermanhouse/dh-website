from django.conf.urls import url

from . import views

app_name = 'menu'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<date>[0-9]+[\/][0-9]+[\/][0-9]+)/$', views.index, name='index'),
    url(r'^add_menu/$', views.add_menu, name='add_menu'),
    url(r'^submit_menu/$', views.submit_menu, name='submit_menu'),
    url(r'^display_meal/(?P<pk>[0-9]+)/$', views.view_meal, name='display_meal'),
    url(r'^add_lateplate/(?P<meal_pk>[0-9]+)/(?P<user_pk>[0-9]+)/$', views.add_lateplate, name='add_lateplate'),
    url(r'^remove_lateplate/(?P<lateplate_pk>[0-9]+)/(?P<user_pk>[0-9]+)/$', views.remove_lateplate, name='remove_lateplate'),
    url(r'^shopper/(?P<pk>[0-9]+)/$', views.shopper, name='shopper'),
    url(r'^auto_lateplates/$', views.auto_lateplates, name='auto_lateplates'),
    url(r'^submit_auto_lateplates/$', views.submit_auto_lateplates, name="submit_auto_lateplates"),
    url(r'^ingredient_info/(?P<ing>[0-9]+)[\/](?P<menu>[0-9]+)/$', views.ingredient_info, name='ingredient_info'),
    url(r'^rate_meal/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="rate_meal"),
    url(r'^submit_rating/(?P<pk>[0-9]+)/', views.submit_rating, name="submit_rating"),
    url(r'^menu_reviews/', views.see_reviews, name="menu_reviews")
]

