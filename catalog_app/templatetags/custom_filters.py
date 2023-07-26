# catalog_app/templatetags/custom_filters.py

from django import template
from django.template.defaultfilters import truncatechars
from django.templatetags.static import static

register = template.Library()


@register.filter
def mediapath(image_path):
    # Формируем полный путь к медиафайлу, добавляя префикс '/media/'
    return f"/media/{image_path}"


@register.filter
def truncate_description(description, length=100):
    # Обрезаем описание до первых 100 символов
    return truncatechars(description, length)
