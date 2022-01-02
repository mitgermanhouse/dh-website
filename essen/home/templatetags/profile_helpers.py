from django import template

register = template.Library()
# from django.contrib.auth.models import User
# from profiles.models import Member

@register.filter(is_safe = True)
def name_or_edit(var):
    try:
        name = var.get_full_name().strip()
        if name != "":
            return name
    except:
        pass
    return "Edit Profile"
