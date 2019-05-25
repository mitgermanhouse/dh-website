from django.conf.urls import url

from . import views

app_name = 'recipes'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditView.as_view(), name='edit'),
    url(r'^(?P<recipe_id>[0-9]+)/submit_edit/$', views.submit_edit, name='submit_edit'),
    url(r'^add/$', views.add_recipe, name='add_recipe'),
    url(r'^add/submit_recipe', views.submit_recipe, name="submit_recipe"),
]

