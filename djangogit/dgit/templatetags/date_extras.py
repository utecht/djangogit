import datetime

from django import template

register = template.Library()

@register.filter
def date_from_unix(value):
    return datetime.datetime.fromtimestamp(long(value)) #.strftime('%Y-%m-%d %H:%M:%S')