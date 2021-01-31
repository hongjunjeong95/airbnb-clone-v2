from django import template

register = template.Library()


@register.simple_tag
def remainder_op(index):
    return index % 4
