from django import template

register = template.Library()
from datetime import datetime, timedelta

import html

@register.filter(is_safe = True)
def decode(var):
    return html.unescape(var)
