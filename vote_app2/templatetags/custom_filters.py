from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def localtime(value):
    """Convert a datetime object to local time."""
    if value is None:
        return ''
    local_time = timezone.localtime(value)
    return local_time.strftime('%d/%m/%Y %H:%M:%S')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def floatdiv(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0