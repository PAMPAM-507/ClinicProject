from django import template

# from ClinicWebsite.models import *

register = template.Library()


@register.filter()
def create_range(value, start_index=0):
    return range(start_index, value + start_index)


@register.filter()
def last_chars(value):
    return value[-3:]


@register.filter()
def check_int(value):
    if type(value) == int:
        return True
    return False
