from django import template

register = template.Library()
# from django.contrib.auth.models import User
# from profiles.models import Member

@register.filter(is_safe = True)
def member_or_none(var):
    try:
        member = var.member
        return "Welcome back, " + var.get_full_name() + "!"
    except:
        return "Hi " + var.get_full_name() + ", edit your profile here!"
