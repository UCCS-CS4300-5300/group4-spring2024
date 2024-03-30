from django import template

register = template.Library()

@register.filter(name='is_owner')
def is_owner(user):
    return user.groups.filter(name='Owner').exists()
