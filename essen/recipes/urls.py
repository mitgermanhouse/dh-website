from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.RecipesListView.as_view(), name='index'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.RecipeEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='delete'),
    path('add/', views.RecipeAddView.as_view(), name='add'),
]

