from django import template
from main.models import MenuItem


register = template.Library()


@register.inclusion_tag("menu.html")
def draw_menu(name):
    query_set = MenuItem.objects.filter(menu=name).select_related("menu").select_related("child_item").order_by("level_index").order_by("column_index")
    return {
        "data": query_set,
        "menu_name": next(iter(query_set)).menu.name
    }
