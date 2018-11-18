from django import template

register = template.Library()


@register.filter(name='loop_range')
def loop_range(number):
    return range(number)

