from django.contrib import admin

from home.models import Member, DietaryRestriction, GalleryContent

class MemberAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name']

admin.site.register(Member, MemberAdmin)
admin.site.register(DietaryRestriction)
admin.site.register(GalleryContent)