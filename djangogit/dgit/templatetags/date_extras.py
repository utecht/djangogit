import datetime

from django import template

register = template.Library()

@register.filter
def date_from_unix(value):
    return datetime.datetime.fromtimestamp(long(value)) #.strftime('%Y-%m-%d %H:%M:%S')

@register.filter
def short_message(value):
    """grab the short version of a commit message"""
    try:
        return value[:value.find('\n')]
    except:
        return "***failed to shorten message :(" 