from django import template
from django.contrib.auth.models import Group
register = template.Library()

@register.filter
def dict_value(value: dict, key):
    return value.get(key, " ")


@register.filter
def in_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    return True if group in user.groups.all() else False
