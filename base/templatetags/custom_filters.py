from django import template

register = template.Library()

# Add custom template filter to subtract by 1
@register.filter
def subtract_one(value):
    return value - 1