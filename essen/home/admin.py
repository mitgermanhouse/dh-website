from django.contrib import admin

from home.models import Member, DietaryRestriction

class MemberAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name']

admin.site.register(Member, MemberAdmin)
admin.site.register(DietaryRestriction)