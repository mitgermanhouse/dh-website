from django import template

register = template.Library()
from datetime import datetime, timedelta

import HTMLParser
html_parser = HTMLParser.HTMLParser()

@register.filter(is_safe = True)
def decode(var):
    return html_parser.unescape(var)