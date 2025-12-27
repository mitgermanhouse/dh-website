from django.urls import path

from . import views

app_name = "menu"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<y-m-d:date>/", views.IndexView.as_view(), name="index"),
    path("add/", views.MenuAddView.as_view(), name="add_menu"),
    path("add/<y-m-d:date>/", views.MenuAddView.as_view(), name="add_menu"),
    path("meal/latest/", views.LatestMealRedirectView.as_view(), name="latest_meal"),
    path("meal/latest/<path:suffix>/", views.LatestMealRedirectView.as_view(), name="latest_meal_with_suffix"),
    path("<int:pk>/edit/", views.MenuEditView.as_view(), name="edit_menu"),
    path("<int:pk>/delete/", views.MenuDeleteView.as_view(), name="delete_menu"),
    path("meal/<int:pk>/", views.MealView.as_view(), name="display_meal"),
    path(
        "meal/<int:pk>/lateplate/",
        views.ModifyLateplate.as_view(),
        name="modify_lateplate",
    ),
    path("meal/<int:pk>/rate/", views.RateMealView.as_view(), name="rate_meal"),
    path("shopper/<int:pk>/", views.ShopperView.as_view(), name="shopper"),
    path("shopper/<int:pk>.tsv", views.ShopperTSV.as_view(), name="shopper_tsv"),
    path("menu_reviews/", views.ReviewsView.as_view(), name="menu_reviews"),
]
