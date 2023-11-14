from django import template
from main.models import MenuItem


register = template.Library()
exists_items = []


@register.inclusion_tag("menu.html")
def draw_menu(name):
    query_set = MenuItem.objects.select_related("child_item", "menu").filter(menu=name).order_by("level_index").order_by("column_index")
    return {
        "exists_items": exists_items,
        "data": query_set,
        "menu_name": next(iter(query_set)).menu.name
    }


@register.inclusion_tag("menu_item.html", takes_context=True)
def recursion_in(context, item):
    child_item = item.child_item
    if not child_item:
        if item.pk in exists_items:
            return context
        context["item"] = item
        exists_items.append(item.pk)
        return context
    if item.pk in exists_items and child_item.pk in exists_items:
        return context
    if item.pk in exists_items:
        context["child_item"] = child_item
        exists_items.append(child_item.pk)
    elif child_item.pk in exists_items:
        context["item"] = item
        exists_items.append(item.pk)
    else:
        context["item"] = item
        context["child_item"] = child_item
        exists_items.append(item.pk)
        exists_items.append(child_item.pk)
    return context
