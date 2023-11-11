from django import template
from django.template.loader import render_to_string
from main.models import Menu, MenuItem


register = template.Library()


@register.simple_tag()
def draw_menu(name):
    query_set = MenuItem.objects.filter(menu=name).select_related("menu").select_related("parent_item").order_by("level_index").order_by("column_index")
    template_ = render_to_string("menu.html", context={

        "data": query_set,
        "menu_name": next(iter(query_set)).menu.name
    })
    return template_
