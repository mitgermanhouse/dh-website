from django.contrib import admin
from .models import Alumnus

@admin.register(Alumnus)
class AlumnusAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'kerb', 'year')
    search_fields = ('first_name', 'last_name', 'kerb', 'year')
    list_filter = ('year',)
