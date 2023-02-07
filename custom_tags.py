import jinja2
from django import template

register = template.Library()

@register.filter
def in_category(things, category):
    return things.filter(category=category)
jinja2.filters.FILTERS['in_category'] = in_category
