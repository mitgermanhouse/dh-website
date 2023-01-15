from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "user/create_profile/", views.ProfileCreateView.as_view(), name="create_profile"
    ),
    path("user/edit_profile/", views.ProfileUpdateView.as_view(), name="edit_profile"),
    path(
        "user/edit_profile/plushies/<int:pk>/edit/",
        views.PlushieEditView.as_view(),
        name="edit_plushie",
    ),
    path(
        "user/edit_profile/plushies/<int:pk>/delete/",
        views.PlushieDeleteView.as_view(),
        name="delete_plushie",
    ),
    path(
        "user/edit_profile/plushies/add/",
        views.PlushieAddView.as_view(),
        name="add_plushie",
    ),
    path("user/dining/", views.DiningUpdateView.as_view(), name="edit_dining"),
]
