# catalog_app/templatetags/custom_filters.py

from django import template
from django.template.defaultfilters import truncatechars
from django.templatetags.static import static

register = template.Library()


@register.filter
def truncate_description(description, length=100):
    # Обрезаем описание до первых 100 символов
    return truncatechars(description, length)
