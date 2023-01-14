from datetime import timedelta

from django import template

register = template.Library()


@register.filter(is_safe=True)
def mult(var, args):
    return var * args


@register.filter(is_safe=True)
def div(var, args):
    return round(var / args, 2)


@register.filter(is_safe=True)
def changedate(var, args):
    return var + timedelta(days=args)
