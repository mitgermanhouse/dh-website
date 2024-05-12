from django.contrib import admin

from essen.helper import compress_image_upload
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
class GalleryContentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Handle image compression
        obj.image = compress_image_upload(obj.image, max_width=4000, max_height=4000)
        super().save_model(request, obj, form, change)


admin.site.register(DietaryRestriction)
admin.site.register(Plushie)
