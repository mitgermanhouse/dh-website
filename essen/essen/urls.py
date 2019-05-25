from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('recipes/', include('recipes.urls')),
    path('essen/', include('menu.urls')),
    path('admin/', admin.site.urls),
]
