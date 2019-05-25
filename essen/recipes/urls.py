from django.urls import path, re_path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/edit/$', views.EditView.as_view(), name='edit'),
    re_path(r'^(?P<recipe_id>[0-9]+)/submit_edit/$', views.submit_edit, name='submit_edit'),
    re_path(r'^add/$', views.add_recipe, name='add_recipe'),
    re_path(r'^add/submit_recipe', views.submit_recipe, name="submit_recipe"),
]

