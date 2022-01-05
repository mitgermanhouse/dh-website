from django.conf.urls import url

from . import views

app_name = 'recipes'
urlpatterns = [
    url(r'^$', views.RecipesListView.as_view(), name='index'),
    url(r'(?P<pk>[0-9]+)/$', views.RecipeDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.RecipeEditView.as_view(), name='edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.RecipeDeleteView.as_view(), name='delete'),
    url(r'^add/$', views.RecipeAddView.as_view(), name='add'),
]

