from django import template

register = template.Library()


@register.filter
def range_filter(value):
    return range(1, value + 1)


@register.filter
def convert_to_int(value):
    return int(value)
