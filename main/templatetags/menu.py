from django import template
from django.template.loader import render_to_string
from main.models import Menu, MenuItem


register = template.Library()


@register.simple_tag()
def draw_menu(name):
    return {"data": MenuItem.objects.select_related("parent_item").select_related("menu").filter(menu=name)}
