from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from .models import Alumnus
from .forms import AddAlumniForm
from .utils import import_alumni_from_xlsx

@admin.register(Alumnus)
class AlumnusAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'kerb', 'year')
    search_fields = ('first_name', 'last_name', 'kerb', 'year')
    list_filter = ('year',)
    change_list_template = "admin/alumni/alumnus/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add-bulk/', self.admin_site.admin_view(self.add_bulk), name='alumni_alumnus_add_bulk'),
        ]
        return my_urls + urls

    def add_bulk(self, request):
        if request.method == "POST":
            form = AddAlumniForm(request.POST, request.FILES)
            if form.is_valid():
                xlsx_file = request.FILES["xlsx_file"]
                try:
                    count = import_alumni_from_xlsx(xlsx_file)
                    self.message_user(request, f"Successfully imported {count} alumni.", messages.SUCCESS)
                    return redirect("admin:alumni_alumnus_changelist")
                except Exception as e:
                    self.message_user(request, f"Error importing file: {e}", messages.ERROR)
        else:
            form = AddAlumniForm()
        
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            opts=self.model._meta,
        )
        return render(request, "admin/alumni/add_alumni.html", context)
