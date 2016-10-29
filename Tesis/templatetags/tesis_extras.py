from django import template

register = template.Library()

@register.filter
def concatenar(num):
    return "form.extra_field_"+str(num)

def lower(value):
    return value.lower()