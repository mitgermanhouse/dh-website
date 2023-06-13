from django.contrib import admin

from faqs.models import Category, Faq


class FaqAdmin(admin.ModelAdmin):
    search_fields = ["question", "id"]


admin.site.register(Faq, FaqAdmin)
admin.site.register(Category)
