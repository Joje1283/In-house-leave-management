from django import template

register = template.Library()


@register.filter
def is_group(member, name):
    return member.is_group(name)
