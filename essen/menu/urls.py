from django.conf.urls import url

from . import views

app_name = 'menu'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<date>[0-9]+-[0-9]+-[0-9]+)/$', views.IndexView.as_view(), name='index'),
    url(r'^meal/(?P<pk>[0-9]+)/$', views.MealView.as_view(), name='display_meal'),
    url(r'^meal/(?P<pk>[0-9]+)/lateplate$', views.ModifyLateplate.as_view(), name='modify_lateplate'),
    url(r'^meal/(?P<pk>[0-9]+)/rate/$', views.RateMealView.as_view(), name='rate_meal'),
    url(r'^menu/add$', views.MenuAddView.as_view(), name='add_menu'),
    url(r'^menu/add/(?P<date>[0-9]+-[0-9]+-[0-9]+)/$', views.MenuAddView.as_view(), name='add_menu'),
    url(r'^menu/(?P<pk>[0-9]+)/edit$', views.MenuEditView.as_view(), name='edit_menu'),
    url(r'^menu/(?P<pk>[0-9]+)/delete$', views.MenuDeleteView.as_view(), name='delete_menu'),
    url(r'^shopper/(?P<pk>[0-9]+)/$', views.ShopperView.as_view(), name='shopper'),
    url(r'^menu_reviews/', views.ReviewsView.as_view(), name="menu_reviews")
]

