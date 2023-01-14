from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "user/create_profile/", views.ProfileCreateView.as_view(), name="create_profile"
    ),
    path("user/edit_profile/", views.ProfileUpdateView.as_view(), name="edit_profile"),
    path("user/dining/", views.DiningUpdateView.as_view(), name="edit_dining"),
]
