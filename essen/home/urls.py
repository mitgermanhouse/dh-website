from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('edit_profile/', views.EditProfileUpdateView.as_view(), name='edit_profile'),
]