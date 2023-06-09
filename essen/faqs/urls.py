from django.urls import path

from . import feeds, views

app_name = "faqs"
urlpatterns = [
    path("", views.FaqsListView.as_view(), name="index"),
    path("<int:pk>/", views.FaqDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.FaqEditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.FaqDeleteView.as_view(), name="delete"),
    path("add/", views.FaqAddView.as_view(), name="add"),
    path("feed/", feeds.FaqsFeed()),
]
