from adminsortable.admin import SortableAdmin
from django.contrib import admin

from home.models import DietaryRestriction, GalleryContent, Member, Plushie


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ("user__first_name", "user__last_name")
    list_display = ("display_first_name", "display_last_name", "display_is_active")
    ordering = ("-user__is_active", "user__first_name", "user__last_name")

    @admin.display(description="First Name", ordering="user__first_name")
    def display_first_name(self, obj: Member):
        return obj.user.first_name

    @admin.display(description="Last Name", ordering="user__last_name")
    def display_last_name(self, obj: Member):
        return obj.user.last_name

    @admin.display(description="Is Active", boolean=True, ordering="user__is_active")
    def display_is_active(self, obj: Member):
        return obj.user.is_active


@admin.register(GalleryContent)
class GalleryContentAdmin(SortableAdmin):
    pass


admin.site.register(DietaryRestriction)
admin.site.register(Plushie)
