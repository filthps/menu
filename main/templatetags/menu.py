from django import template
from main.models import MenuItem


register = template.Library()


@register.inclusion_tag("menu.html")
def draw_menu(name):
    query_set = MenuItem.objects.select_related("child_item", "menu").filter(menu=name).order_by("column_index")
    try:
        menu_name = next(iter(query_set)).menu.name
    except StopIteration:
        menu_name = None
    return {
        "exists_items": set(),
        "data": query_set,
        "menu_name": menu_name
    }


@register.inclusion_tag("menu_item.html", takes_context=True)
def recursion_in(context, item, from_loop=False):
    child_item = item.child_item
    if not from_loop:
        context["item"] = item
        context["child_item"] = child_item
        context["exists_items"].add(child_item.pk) if child_item else None
        context["exists_items"].add(item.pk)
        return context
    context["child_item"] = None
    context["item"] = None
    if child_item:
        if child_item.pk not in context["exists_items"]:
            context["child_item"] = child_item
            context["exists_items"].add(child_item.pk)
    if item.pk not in context["exists_items"]:
        context["item"] = item
        context["exists_items"].add(item.pk)
    return context
