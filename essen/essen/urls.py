from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import include, path, register_converter
from django.views.generic.base import RedirectView
from django.views.static import serve

from essen.converters import DateConverter

register_converter(DateConverter, "y-m-d")

urlpatterns = [
    path("", lambda r: HttpResponseRedirect("home/")),
    path("recipes/", include("recipes.urls")),
    path("menu/", include("menu.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("home/", include("home.urls")),
    path("mit/", include("mit.urls")),
    path("essen", RedirectView.as_view(url="menu/")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("icon/favicon.ico")),
    ),
    path("ping", lambda r: HttpResponse("The website is running.")),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "media/<path:path>/",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        )
    ]

    from django.apps import apps

    if apps.is_installed("debug_toolbar"):
        urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
